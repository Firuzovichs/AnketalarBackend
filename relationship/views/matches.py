from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from relationship.models import Relationship, RelationStatus
from relationship.serializers.matches import MatchSerializer

class MatchesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = (
            Relationship.objects
            .filter(from_user=request.user, status=RelationStatus.MATCHED)
            .select_related("to_user")
            .order_by("-updated_at")
        )
        return Response(MatchSerializer(qs, many=True).data)
