from rest_framework import serializers
from accounts.models import UserProfile, UserPhoto

class MeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nickname = serializers.CharField()
    phone = serializers.CharField(allow_null=True)
    email = serializers.EmailField(allow_null=True)

    phone_verified = serializers.BooleanField()
    email_verified = serializers.BooleanField()

    face_status = serializers.CharField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()

    profile_exists = serializers.BooleanField()
    profile_completed = serializers.BooleanField()
    photo_count = serializers.IntegerField()
    main_photo_url = serializers.CharField(allow_null=True)

    next_action = serializers.CharField()
