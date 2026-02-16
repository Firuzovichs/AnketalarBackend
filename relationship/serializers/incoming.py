from rest_framework import serializers
from relationship.models import Relationship

class IncomingLikeSerializer(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField(source="from_user.id", read_only=True)
    from_nickname = serializers.CharField(source="from_user.nickname", read_only=True)

    # comment ham ko'rinsin
    comment = serializers.CharField(read_only=True)
    comment_liked_at = serializers.DateTimeField(read_only=True, allow_null=True)

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Relationship
        fields = (
            "id",
            "from_user_id",
            "from_nickname",
            "comment",
            "comment_liked_at",
            "created_at",
        )
