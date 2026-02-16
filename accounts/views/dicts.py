from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.models import Interest, Purpose

class InterestListView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "dicts"

    def get(self, request):
        qs = Interest.objects.filter(is_active=True).order_by("name")
        data = [{"id": x.id, "name": x.name} for x in qs]
        return Response(data, status=status.HTTP_200_OK)

class PurposeListView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "dicts"

    def get(self, request):
        qs = Purpose.objects.filter(is_active=True).order_by("name")
        data = [{"id": x.id, "name": x.name} for x in qs]
        return Response(data, status=status.HTTP_200_OK)
