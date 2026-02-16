from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.serializers import VerifyOTPSerializer
from accounts.serializers.resend_otp import ResendOTPSerializer


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    # throttle_scope = "auth_verify"

    

    def post(self, request):
        print(request.data)
        s = VerifyOTPSerializer(data=request.data)
        s.is_valid(raise_exception=True)  

        return Response(
            {"message": "Muvaffaqqiyatli tasdiqlandi"}, 
            status=status.HTTP_200_OK
        )

class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth_resend"

    def post(self, request):
        s = ResendOTPSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        result = s.save()

        resp = {"message": "OTP yuborildi", "channel": result["channel"]}
        if "otp_id" in result:
            resp.update({"otp_id": str(result["otp_id"]), "expires_in": result["expires_in"], "next": "verify_otp"})
        else:
            resp.update({"tg_link_token": str(result["tg_link_token"]), "next": "telegram_link"})

        return Response(resp, status=status.HTTP_200_OK)
