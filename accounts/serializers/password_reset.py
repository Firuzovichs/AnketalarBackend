from rest_framework import serializers
from accounts.services.password_reset_service import (
    start_password_reset,
    confirm_password_reset,
    finish_password_reset,
    ResetError,
)

class ForgotPasswordSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=32)
    channel = serializers.ChoiceField(choices=["email", "telegram"])

    def create(self, validated_data):
        try:
            return start_password_reset(**validated_data)
        except ResetError as e:
            raise serializers.ValidationError({"error": e.code})


class ConfirmResetSerializer(serializers.Serializer):
    reset_id = serializers.UUIDField()
    code = serializers.CharField(max_length=10)

    def create(self, validated_data):
        try:
            return confirm_password_reset(reset_id=str(validated_data["reset_id"]), code=validated_data["code"])
        except ResetError as e:
            raise serializers.ValidationError({"error": e.code})


class ResetPasswordSerializer(serializers.Serializer):
    reset_token = serializers.UUIDField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        try:
            return finish_password_reset(
                reset_token=str(validated_data["reset_token"]),
                new_password=validated_data["new_password"],
            )
        except ResetError as e:
            raise serializers.ValidationError({"error": e.code})
