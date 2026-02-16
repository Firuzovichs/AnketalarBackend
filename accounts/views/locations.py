from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.models import Region, District

class RegionListView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "dicts"

    def get(self, request):
        qs = Region.objects.all().order_by("order", "name")
        return Response([{"id": r.id, "name": r.name} for r in qs], status=status.HTTP_200_OK)

class DistrictListView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "dicts"

    def get(self, request):
        region_id = request.query_params.get("region_id")
        qs = District.objects.all().select_related("region").order_by("order", "name")
        if region_id:
            qs = qs.filter(region_id=region_id)
        return Response([{"id": d.id, "name": d.name, "region_id": d.region_id} for d in qs], status=status.HTTP_200_OK)
