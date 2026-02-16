from rest_framework import serializers
from accounts.models import User
from accounts.services.auth_service import confirm_otp


class VerifyOTPSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=32)
    otp_id = serializers.UUIDField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        nickname = attrs["nickname"].strip().lower()
        if not User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError("User topilmadi")

        try:
            confirm_otp(nickname=nickname, otp_id=attrs["otp_id"], code=attrs["code"])
        except ValueError as e:
            error_type = str(e)
            if error_type == "invalid_code":
                raise serializers.ValidationError({"code": "Kod noto‘g‘ri"})
            elif error_type == "expired":
                raise serializers.ValidationError({"code": "Kod muddati tugagan"})
            else:
                raise serializers.ValidationError("OTP xato")

        return attrs
