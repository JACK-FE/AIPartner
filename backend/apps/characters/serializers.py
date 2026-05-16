from rest_framework import serializers
from .models import AICharacter, ModelConfig, Follow
from .voice_presets import PRESET_BY_KEY


class ModelConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelConfig
        fields = ("id", "provider", "model_name", "sort_order")
        read_only_fields = ("id",)


class AICharacterListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.username", read_only=True)
    model_name = serializers.CharField(source="model.model_name", read_only=True)
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = AICharacter
        fields = (
            "id", "name", "avatar", "description", "personality", "is_public",
            "follow_count", "creator_name", "model_name",
            "is_followed", "voice_preset", "model", "created_at",
        )

    def get_is_followed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follow.objects.filter(user=request.user, character=obj).exists()
        return False


class AICharacterDetailSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.username", read_only=True)
    model_name = serializers.CharField(source="model.model_name", read_only=True)
    model_provider = serializers.CharField(source="model.provider", read_only=True)
    is_followed = serializers.SerializerMethodField()
    voice_label = serializers.SerializerMethodField()
    voice_id = serializers.SerializerMethodField()

    class Meta:
        model = AICharacter
        fields = (
            "id", "name", "avatar", "description", "personality",
            "system_prompt", "is_public", "follow_count",
            "creator_name", "model_name", "model_provider",
            "is_followed", "voice_preset", "voice_label", "voice_id",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "creator", "system_prompt",
                            "follow_count", "created_at", "updated_at")

    def get_is_followed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follow.objects.filter(user=request.user, character=obj).exists()
        return False

    def get_voice_label(self, obj):
        preset = PRESET_BY_KEY.get(obj.voice_preset)
        return preset["label"] if preset else ""

    def get_voice_id(self, obj):
        preset = PRESET_BY_KEY.get(obj.voice_preset)
        return preset["voice_id"] if preset else ""


class AICharacterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AICharacter
        fields = (
            "id", "name", "avatar", "description", "personality",
            "model", "voice_preset", "is_public",
        )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class FollowSerializer(serializers.ModelSerializer):
    character = AICharacterListSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "character", "created_at")
