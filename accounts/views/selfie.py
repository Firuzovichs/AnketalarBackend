from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.serializers import UploadSelfieSerializer


class UploadSelfieView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "auth_selfie"

    def post(self, request):
        s = UploadSelfieSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save(user=request.user)

        # request.user face_status task trigger qilgandan keyin yangilanmagan bo'lishi mumkin
        request.user.refresh_from_db(fields=["face_status"])

        return Response(
            {
                "message": "Selfie qabul qilindi. Tekshiruv boshlandi.",
                "face_status": request.user.face_status,
            },
            status=status.HTTP_201_CREATED,
        )
