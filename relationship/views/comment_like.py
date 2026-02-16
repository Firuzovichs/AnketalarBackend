from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404

from accounts.models import User
from relationship.serializers.comment_like_action import CommentLikeActionSerializer
from relationship.services.relationship_service import comment_like
from relationship.services.quota_service import consume_quota

class CommentLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        s = CommentLikeActionSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        liker = get_object_or_404(User, id=s.validated_data["liker_user_id"])

        consume_quota(request.user, "comment_like")
        comment_like(actor=request.user, liker=liker)

        return Response({"ok": True}, status=status.HTTP_200_OK)
