from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "role", "content", "created_at")
        read_only_fields = ("id", "created_at")


class ConversationSerializer(serializers.ModelSerializer):
    character_name = serializers.CharField(source="character.name", read_only=True)
    character_avatar = serializers.CharField(source="character.avatar", read_only=True)
    character_id = serializers.IntegerField(source="character.id", read_only=True)

    class Meta:
        model = Conversation
        fields = ("id", "character_id", "character_name", "character_avatar",
                  "last_message_at", "created_at")
        read_only_fields = ("id", "created_at")


class MessageInputSerializer(serializers.Serializer):
    content = serializers.CharField(min_length=1, max_length=4096)
