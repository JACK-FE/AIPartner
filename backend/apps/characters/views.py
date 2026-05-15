import os
import uuid
import time
import hashlib
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.db.models import Q
from .models import AICharacter, ModelConfig, Follow
from .serializers import (
    AICharacterListSerializer,
    AICharacterDetailSerializer,
    AICharacterCreateSerializer,
    ModelConfigSerializer,
    FollowSerializer,
)
from .voice_presets import PRESET_BY_KEY
from .tts.edge_tts import EdgeTTSProvider


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user


class ModelConfigListView(generics.ListAPIView):
    queryset = ModelConfig.objects.filter(is_active=True)
    serializer_class = ModelConfigSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class CharacterListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AICharacterCreateSerializer
        return AICharacterListSerializer

    def get_queryset(self):
        qs = AICharacter.objects.filter(is_public=True).select_related("creator", "model")
        search = self.request.query_params.get("search", "")
        sort = self.request.query_params.get("sort", "new")
        model_id = self.request.query_params.get("model_id", "")

        if search:
            qs = qs.filter(name__icontains=search)

        if model_id:
            qs = qs.filter(model_id=model_id)

        if sort == "hot":
            qs = qs.order_by("-follow_count", "-created_at")
        else:
            qs = qs.order_by("-created_at")

        return qs

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MyCharacterListView(generics.ListAPIView):
    serializer_class = AICharacterListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return AICharacter.objects.filter(creator=self.request.user).select_related("creator", "model")


class CharacterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AICharacter.objects.all()
    permission_classes = (IsCreatorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return AICharacterCreateSerializer
        return AICharacterDetailSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if "personality" in serializer.validated_data:
            from .models import SYSTEM_PROMPT_TEMPLATE
            instance.system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
                name=instance.name, personality=instance.personality
            )
            instance.save(update_fields=["system_prompt"])


class FollowCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        character_id = kwargs.get("character_id")
        try:
            character = AICharacter.objects.get(id=character_id)
        except AICharacter.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

        follow, created = Follow.objects.get_or_create(
            user=request.user, character=character
        )
        if created:
            character.follow_count += 1
            character.save(update_fields=["follow_count"])
            return Response({"status": "followed"}, status=status.HTTP_201_CREATED)
        return Response({"status": "already_followed"}, status=status.HTTP_200_OK)


class FollowDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        character_id = kwargs.get("character_id")
        try:
            follow = Follow.objects.get(user=request.user, character_id=character_id)
            character = follow.character
            follow.delete()
            character.follow_count = max(0, character.follow_count - 1)
            character.save(update_fields=["follow_count"])
            return Response({"status": "unfollowed"}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({"detail": "Not following."}, status=status.HTTP_404_NOT_FOUND)


class FollowListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user).select_related("character__creator", "character__model")


class CharacterAvatarUploadView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES.get("avatar")
        if not file:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        ext = os.path.splitext(file.name)[1] or ".png"
        filename = f"characters/{request.user.id}_{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        url = request.build_absolute_uri(f"{settings.MEDIA_URL}{filename}")
        return Response({"avatar": url})


def _cleanup_old_tts_files(tts_dir: str, max_age_seconds: int = 86400):
    """清理超过 max_age_seconds 的 TTS 文件。"""
    if not os.path.exists(tts_dir):
        return
    now = time.time()
    for filename in os.listdir(tts_dir):
        filepath = os.path.join(tts_dir, filename)
        if os.path.isfile(filepath) and (now - os.path.getmtime(filepath)) > max_age_seconds:
            try:
                os.remove(filepath)
            except OSError:
                pass


def _run_async(coro):
    """在同步上下文中运行异步协程。"""
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop is not None and loop.is_running():
        # 在已有事件循环中运行（如某些 ASGI 环境）
        import concurrent.futures
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        return future.result(timeout=120)
    return asyncio.run(coro)


class CharacterTTSView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, character_id):
        try:
            character = AICharacter.objects.get(id=character_id)
        except AICharacter.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

        text = request.data.get("text", "")
        if not text:
            return Response({"detail": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)

        preset_key = character.voice_preset
        preset = PRESET_BY_KEY.get(preset_key, PRESET_BY_KEY["shaonv"])

        tts_dir = os.path.join(settings.MEDIA_ROOT, "tts")
        os.makedirs(tts_dir, exist_ok=True)
        _cleanup_old_tts_files(tts_dir)

        text_hash = hashlib.md5(f"{preset_key}:{text}".encode()).hexdigest()[:12]
        filename = f"{int(time.time())}_{text_hash}.mp3"
        filepath = os.path.join(tts_dir, filename)

        provider = EdgeTTSProvider()
        try:
            audio_bytes = _run_async(provider.synthesize(text, preset_key))
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": f"TTS synthesis failed: {e}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        with open(filepath, "wb") as f:
            f.write(audio_bytes)

        url = request.build_absolute_uri(f"{settings.MEDIA_URL}tts/{filename}")
        return Response({"audio_url": url})


class TTSPreviewView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        voice_preset = request.data.get("voice_preset", "shaonv")
        text = request.data.get("text", "")
        if not text:
            return Response({"detail": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 用 preset key 而非硬编码 voice_id，让 provider 做动态匹配
        tts_dir = os.path.join(settings.MEDIA_ROOT, "tts")
        os.makedirs(tts_dir, exist_ok=True)
        _cleanup_old_tts_files(tts_dir)

        text_hash = hashlib.md5(f"{voice_preset}:{text}".encode()).hexdigest()[:12]
        filename = f"preview_{int(time.time())}_{text_hash}.mp3"
        filepath = os.path.join(tts_dir, filename)

        provider = EdgeTTSProvider()
        try:
            audio_bytes = _run_async(provider.synthesize(text, voice_preset))
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": f"TTS synthesis failed: {e}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        with open(filepath, "wb") as f:
            f.write(audio_bytes)

        url = request.build_absolute_uri(f"{settings.MEDIA_URL}tts/{filename}")
        return Response({"audio_url": url})
