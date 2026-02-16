from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from accounts.models import UserPhoto
from accounts.serializers.photo import UserPhotoSerializer, UploadPhotoSerializer

class UserPhotoListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "photo_upload"

    def get(self, request):
        qs = UserPhoto.objects.filter(user=request.user).order_by("-is_main", "order", "-created_at")
        return Response(UserPhotoSerializer(qs, many=True).data)

    def post(self, request):
        s = UploadPhotoSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        photo = UserPhoto.objects.create(
            user=request.user,
            image=s.validated_data["image"],
            is_main=s.validated_data.get("is_main", False),
            order=s.validated_data.get("order", 0),
        )
        return Response(UserPhotoSerializer(photo).data, status=status.HTTP_201_CREATED)


class UserPhotoDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "photo_delete"

    def delete(self, request, pk: int):
        photo = get_object_or_404(UserPhoto, pk=pk, user=request.user)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPhotoSetMainView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "photo_set_main"

    def patch(self, request, pk: int):
        photo = get_object_or_404(UserPhoto, pk=pk, user=request.user)
        photo.is_main = True
        photo.save()
        return Response({"ok": True, "main_photo_id": str(photo.id)}, status=status.HTTP_200_OK)
