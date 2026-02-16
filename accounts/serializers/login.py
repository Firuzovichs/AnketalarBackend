from rest_framework import serializers
from accounts.services.auth_service import login_user


class LoginSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=32)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            data = login_user(nickname=attrs["nickname"], password=attrs["password"])
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return data
