from rest_framework import serializers
from accounts.models import User
from accounts.services.auth_service import resend_otp_for_user


class ResendOTPSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=32)

    def validate(self, attrs):
        nickname = attrs["nickname"].strip().lower()
        if not User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError("User topilmadi")
        attrs["nickname"] = nickname
        return attrs

    def save(self):
        return resend_otp_for_user(nickname=self.validated_data["nickname"])
