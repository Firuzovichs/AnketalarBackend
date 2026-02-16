from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.serializers.password_reset import (
    ForgotPasswordSerializer,
    ConfirmResetSerializer,
    ResetPasswordSerializer,
)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth_forgot"

    def post(self, request):
        s = ForgotPasswordSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        result = s.save()
        return Response({"message": "OTP yuborildi", **result}, status=status.HTTP_200_OK)


class ConfirmResetView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth_confirm"

    def post(self, request):
        s = ConfirmResetSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        result = s.save()
        return Response({"message": "Reset tasdiqlandi", **result}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth_reset"

    def post(self, request):
        s = ResetPasswordSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response({"message": "Parol yangilandi"}, status=status.HTTP_200_OK)
