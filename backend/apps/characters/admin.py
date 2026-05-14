from django.contrib import admin
from .models import ModelConfig, AICharacter, Follow


class ModelConfigAdmin(admin.ModelAdmin):
    list_display = ("provider", "model_name", "is_active", "sort_order")
    list_filter = ("provider", "is_active")
    search_fields = ("provider", "model_name")
    fields = ("provider", "model_name", "api_key", "api_base_url", "is_active", "sort_order")


class AICharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "creator", "model", "is_public", "follow_count")
    list_filter = ("is_public", "model")
    search_fields = ("name",)


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "character", "created_at")
    list_filter = ("created_at",)


admin.site.register(ModelConfig, ModelConfigAdmin)
admin.site.register(AICharacter, AICharacterAdmin)
admin.site.register(Follow, FollowAdmin)
