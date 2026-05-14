from rest_framework import serializers
from .models import AICharacter, ModelConfig, Follow


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
            "id", "name", "avatar", "description", "is_public",
            "follow_count", "creator_name", "model_name",
            "is_followed", "created_at",
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

    class Meta:
        model = AICharacter
        fields = (
            "id", "name", "avatar", "description", "personality",
            "system_prompt", "is_public", "follow_count",
            "creator_name", "model_name", "model_provider",
            "is_followed", "created_at", "updated_at",
        )
        read_only_fields = ("id", "creator", "system_prompt",
                            "follow_count", "created_at", "updated_at")

    def get_is_followed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follow.objects.filter(user=request.user, character=obj).exists()
        return False


class AICharacterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AICharacter
        fields = (
            "id", "name", "avatar", "description", "personality",
            "model", "is_public",
        )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class FollowSerializer(serializers.ModelSerializer):
    character = AICharacterListSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "character", "created_at")
