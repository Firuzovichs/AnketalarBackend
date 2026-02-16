from rest_framework import serializers
from accounts.models import UserPhoto

class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = ("id", "image", "is_main", "order", "created_at")
        read_only_fields = ("id", "is_main", "created_at")

class UploadPhotoSerializer(serializers.Serializer):
    image = serializers.ImageField()
    is_main = serializers.BooleanField(default=False)
    order = serializers.IntegerField(required=False, default=0)
