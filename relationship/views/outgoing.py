from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from relationship.models import Relationship, RelationStatus
from relationship.serializers.outgoing import OutgoingLikeSerializer

class OutgoingLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = (
            Relationship.objects
            .filter(from_user=request.user, status=RelationStatus.LIKED)
            .select_related("to_user")
            .order_by("-created_at")
        )
        return Response(OutgoingLikeSerializer(qs, many=True).data)
