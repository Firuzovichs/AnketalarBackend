from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404

from accounts.models import User
from relationship.serializers.like_action import LikeActionSerializer
from relationship.services.relationship_service import like_only
from relationship.services.quota_service import consume_quota  # sizdagi daily quota

class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        s = LikeActionSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        target = get_object_or_404(User, id=s.validated_data["target_user_id"])

        consume_quota(request.user, "like")
        result = like_only(actor=request.user, target=target)

        return Response({"ok": True, **result}, status=status.HTTP_200_OK)
