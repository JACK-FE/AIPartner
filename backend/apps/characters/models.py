from django.db import models
from django.conf import settings

from config.crypto import EncryptedCharField

SYSTEM_PROMPT_TEMPLATE = """You are an AI friend named {name}.
Personality: {personality}
In conversation, be friendly, warm, and natural. Respond as a close friend would."""


class ModelConfig(models.Model):
    provider = models.CharField(max_length=32)
    model_name = models.CharField(max_length=64)
    api_key = EncryptedCharField(max_length=512)
    api_base_url = models.CharField(max_length=256, blank=True, default="")
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("sort_order",)

    def __str__(self):
        return f"{self.provider} / {self.model_name}"


class AICharacter(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="characters"
    )
    name = models.CharField(max_length=64)
    avatar = models.URLField(max_length=512, blank=True, default="")
    description = models.TextField(blank=True, default="")
    personality = models.TextField(blank=True, default="")
    system_prompt = models.TextField(blank=True, default="")
    model = models.ForeignKey(
        ModelConfig, on_delete=models.PROTECT, related_name="characters"
    )
    is_public = models.BooleanField(default=True)
    follow_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.system_prompt and self.personality:
            self.system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
                name=self.name, personality=self.personality
            )
        super().save(*args, **kwargs)


class Follow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follows"
    )
    character = models.ForeignKey(
        AICharacter, on_delete=models.CASCADE, related_name="follows"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "character")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.username} -> {self.character.name}"
