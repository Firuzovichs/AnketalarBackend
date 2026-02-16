from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from relationship.models import Relationship, RelationStatus
from relationship.serializers import IncomingLikeSerializer

class IncomingLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = (
            Relationship.objects
            .filter(to_user=request.user, status=RelationStatus.LIKED)
            .select_related("from_user")
            .order_by("-created_at")
        )
        return Response(IncomingLikeSerializer(qs, many=True).data)
