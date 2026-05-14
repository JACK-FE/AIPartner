from django.urls import path
from .views import MessageHistoryView, ConversationListView, ChatStreamView

urlpatterns = [
    path("characters/<int:character_id>/messages/", MessageHistoryView.as_view(), name="message-history"),
    path("characters/<int:character_id>/chat/", ChatStreamView.as_view(), name="chat-stream"),
    path("conversations/", ConversationListView.as_view(), name="conversation-list"),
]
