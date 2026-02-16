from rest_framework import serializers
from django.utils import timezone
from accounts.models import TelegramLinkToken, User

class TelegramLinkConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    chat_id = serializers.IntegerField()

    def validate(self, attrs):
        try:
            t = TelegramLinkToken.objects.select_related("user").get(id=attrs["token"])
        except TelegramLinkToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token")

        if t.is_used or t.is_expired:
            raise serializers.ValidationError("Token expired or used")

        attrs["tg_token"] = t
        return attrs

    def save(self):
        t: TelegramLinkToken = self.validated_data["tg_token"]
        chat_id = self.validated_data["chat_id"]

        # chat_id boshqa userga tegishli bo'lmasin
        if User.objects.filter(telegram_chat_id=chat_id).exclude(id=t.user_id).exists():
            raise serializers.ValidationError("This Telegram account is already linked")

        u = t.user
        u.telegram_chat_id = chat_id
        u.save(update_fields=["telegram_chat_id"])

        t.used_at = timezone.now()
        t.save(update_fields=["used_at"])
        return u
