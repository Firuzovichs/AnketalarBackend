from rest_framework import serializers

class CommentLikeActionSerializer(serializers.Serializer):
    liker_user_id = serializers.IntegerField()
