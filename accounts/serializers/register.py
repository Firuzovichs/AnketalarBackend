from rest_framework import serializers
from accounts.models import User
from accounts.services.auth_service import register_user
import re


class RegisterSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=32)
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol kamida 8 ta belgi bo'lishi kerak")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Parolda kamida 1 ta katta harf bo'lishi kerak")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Parolda kamida 1 ta kichik harf bo'lishi kerak")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Parolda kamida 1 ta raqam bo'lishi kerak")
        return value

    def validate(self, attrs):
        nickname = attrs.get("nickname", "").strip().lower()
        phone = attrs.get("phone") or None
        email = attrs.get("email") or None

        if not phone and not email:
            raise serializers.ValidationError("phone yoki emaildan bittasi majburiy")

        if User.objects.filter(nickname__iexact=nickname).exists():
            raise serializers.ValidationError("Bu nickname band")

        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("Bu telefon raqam band")

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Bu email band")

        attrs["nickname"] = nickname
        attrs["phone"] = phone
        attrs["email"] = email
        return attrs

    def create(self, validated_data):
        return register_user(
            nickname=validated_data["nickname"],
            password=validated_data["password"],
            phone=validated_data["phone"],
            email=validated_data["email"],
            ttl_minutes=5,
        )
