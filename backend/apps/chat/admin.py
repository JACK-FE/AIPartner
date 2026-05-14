from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("role", "content", "created_at")


class ConversationAdmin(admin.ModelAdmin):
    list_display = ("user", "character", "last_message_at")
    inlines = (MessageInline,)


admin.site.register(Conversation, ConversationAdmin)
