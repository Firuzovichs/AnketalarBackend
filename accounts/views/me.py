from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.serializers.me import MeSerializer

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        profile = getattr(user, "profile", None)
        profile_exists = profile is not None
        profile_completed = bool(profile_exists and getattr(profile, "is_profile_complete", False))

        photo_count = user.photos.count()
        main = user.photos.filter(is_main=True).first()
        main_url = main.image.url if main and main.image else None

        # next_action logika
        if user.face_status == "REJECTED":
            next_action = "upload_selfie_again"
        elif user.face_status == "PENDING":
            next_action = "wait_face_review"
        else:
            # APPROVED deb faraz qilamiz
            if not profile_exists:
                next_action = "create_profile"
            elif not profile_completed:
                next_action = "complete_profile"
            elif not main:
                next_action = "upload_main_photo"
            else:
                next_action = "ready"

        data = {
            "id": user.id,
            "nickname": user.nickname,
            "phone": user.phone,
            "email": user.email,
            "phone_verified": user.phone_verified,
            "email_verified": user.email_verified,
            "face_status": user.face_status,
            "is_active": user.is_active,
            "is_staff": user.is_staff,

            "profile_exists": profile_exists,
            "profile_completed": profile_completed,
            "photo_count": photo_count,
            "main_photo_url": main_url,

            "next_action": next_action,
        }

        return Response(MeSerializer(data).data)