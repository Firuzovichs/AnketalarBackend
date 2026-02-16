from rest_framework import serializers
from relationship.models import Relationship

class OutgoingLikeSerializer(serializers.ModelSerializer):
    to_user_id = serializers.IntegerField(source="to_user.id", read_only=True)
    to_nickname = serializers.CharField(source="to_user.nickname", read_only=True)

    # agar siz outgoing'da ham comment saqlasangiz (ixtiyoriy)
    comment = serializers.CharField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Relationship
        fields = ("id", "to_user_id", "to_nickname", "comment", "created_at")
