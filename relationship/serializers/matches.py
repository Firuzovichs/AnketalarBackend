from rest_framework import serializers
from relationship.models import Relationship

class MatchSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="to_user.id", read_only=True)
    nickname = serializers.CharField(source="to_user.nickname", read_only=True)

    # Qarshi tomondan kelgan commentni ham ko'rsatmoqchi bo'lsangiz keyin qo'shamiz
    matched_at = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Relationship
        fields = ("id", "user_id", "nickname", "matched_at")
