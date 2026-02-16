from rest_framework import serializers
from accounts.services.selfie_service import upload_selfie


class UploadSelfieSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def save(self, *, user):
        return upload_selfie(user=user, image=self.validated_data["image"])
