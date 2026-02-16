from rest_framework import serializers

class LikeActionSerializer(serializers.Serializer):
    target_user_id = serializers.IntegerField()
