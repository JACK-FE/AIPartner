from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "avatar", "bio", "date_joined")
        read_only_fields = ("id", "email", "date_joined")


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = "email"

    def validate(self, attrs):
        authenticate_kwargs = {
            "email": attrs.get("email"),
            "password": attrs.get("password"),
        }
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            raise serializers.ValidationError("用户名或密码错误")
        refresh = RefreshToken.for_user(self.user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
