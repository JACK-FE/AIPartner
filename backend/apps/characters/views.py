import os
import uuid
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import AICharacter, ModelConfig, Follow
from .serializers import (
    AICharacterListSerializer,
    AICharacterDetailSerializer,
    AICharacterCreateSerializer,
    ModelConfigSerializer,
    FollowSerializer,
)


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
