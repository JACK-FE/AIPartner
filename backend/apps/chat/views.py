import json
from django.utils import timezone
from django.http import StreamingHttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer, MessageInputSerializer
from .llm import stream_chat


class MessageHistoryView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        character_id = self.kwargs.get("character_id")
        conv = Conversation.objects.filter(
            user=self.request.user, character_id=character_id
        ).first()
        if not conv:
            return Message.objects.none()
        return Message.objects.filter(conversation=conv)


class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).select_related("character")


class ChatStreamView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request, character_id):
        from apps.characters.models import AICharacter, ModelConfig

        serializer = MessageInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        content = serializer.validated_data["content"]

        try:
            character = AICharacter.objects.select_related("model").get(id=character_id)
        except AICharacter.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

        conv, _ = Conversation.objects.get_or_create(
            user=request.user,
            character=character,
        )

        user_msg = Message.objects.create(
            conversation=conv, role="user", content=content
        )

        conv.last_message_at = timezone.now()
        conv.save(update_fields=["last_message_at"])

        history = Message.objects.filter(conversation=conv).order_by("created_at")[:20]
        messages = [
            {"role": "system", "content": character.system_prompt},
        ]
        for m in history:
            messages.append({"role": m.role, "content": m.content})

        def generate():
            full_content = ""
            for token in stream_chat(character.model, messages):
                full_content += token
                yield f"event: token\ndata: {json.dumps({'token': token})}\n\n"

            assistant_msg = Message.objects.create(
                conversation=conv, role="assistant", content=full_content
            )
            conv.last_message_at = timezone.now()
            conv.save(update_fields=["last_message_at"])
            yield f"event: done\ndata: {json.dumps({'message_id': assistant_msg.id})}\n\n"

        response = StreamingHttpResponse(
            generate(),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response
