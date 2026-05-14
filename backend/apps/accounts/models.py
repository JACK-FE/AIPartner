import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser

GRAVATAR_BASE = "https://www.gravatar.com/avatar/"


def gravatar_url(email, size=200):
    h = hashlib.md5(email.lower().encode()).hexdigest()
    return f"{GRAVATAR_BASE}{h}?d=identicon&s={size}"


class User(AbstractUser):
    avatar = models.URLField(max_length=512, blank=True, default="")
    bio = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = gravatar_url(self.email)
        super().save(*args, **kwargs)
