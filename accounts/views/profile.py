from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.models import UserProfile
from accounts.serializers.profile_complete import ProfileCompleteSerializer

class ProfileCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "profile_update"

    def post(self, request):
        if hasattr(request.user, "profile"):
            return Response({"detail": "Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)

        s = ProfileCompleteSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        profile = UserProfile.objects.create(user=request.user, **{
            k: v for k, v in s.validated_data.items()
            if k not in ("interests", "purposes")
        })
        profile.interests.set(s.validated_data["interests"])
        profile.purposes.set(s.validated_data["purposes"])

        return Response(ProfileCompleteSerializer(profile).data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        if not hasattr(request.user, "profile"):
            return Response({"detail": "Profile not found. Use POST first."}, status=status.HTTP_404_NOT_FOUND)

        s = ProfileCompleteSerializer(instance=request.user.profile, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        profile = s.save()

        return Response(ProfileCompleteSerializer(profile).data, status=status.HTTP_200_OK)
