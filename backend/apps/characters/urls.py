from django.urls import path
from .views import (
    ModelConfigListView,
    CharacterListCreateView,
    MyCharacterListView,
    CharacterDetailView,
    FollowCreateView,
    FollowDeleteView,
    FollowListView,
    CharacterAvatarUploadView,
    CharacterTTSView,
    TTSPreviewView,
)

urlpatterns = [
    path("models/", ModelConfigListView.as_view(), name="model-list"),
    path("characters/", CharacterListCreateView.as_view(), name="character-list"),
    path("characters/mine/", MyCharacterListView.as_view(), name="my-characters"),
    path("characters/<int:pk>/", CharacterDetailView.as_view(), name="character-detail"),
    path("characters/<int:character_id>/follow/", FollowCreateView.as_view(), name="follow"),
    path("characters/<int:character_id>/unfollow/", FollowDeleteView.as_view(), name="unfollow"),
    path("follows/", FollowListView.as_view(), name="follow-list"),
    path("characters/avatar/upload/", CharacterAvatarUploadView.as_view(), name="character-avatar-upload"),
    path("characters/<int:character_id>/tts/", CharacterTTSView.as_view(), name="character-tts"),
    path("tts/preview/", TTSPreviewView.as_view(), name="tts-preview"),
]
