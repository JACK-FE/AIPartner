import base64
import hashlib

from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet, InvalidToken


def _get_fernet():
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def encrypt_value(plain):
    return _get_fernet().encrypt(plain.encode()).decode()


def decrypt_value(cipher):
    return _get_fernet().decrypt(cipher.encode()).decode()


class EncryptedCharField(models.CharField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return decrypt_value(value)
        except (InvalidToken, Exception):
            return value

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return value
        return encrypt_value(value)
