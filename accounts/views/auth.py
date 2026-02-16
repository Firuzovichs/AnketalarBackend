from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    # throttle_scope = "auth_register"

    def post(self, request):
        print("RegisterView POST data:", request.data)  
        s = RegisterSerializer(data=request.data)
        if not s.is_valid():
            print("Serializer errors:", s.errors)   
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        result = s.save()
        

        resp = {
            "message": "Registratsiya yaratildi.",
            "nickname": result["user"].nickname,
            "channel": result["channel"],
        }

        if "otp_id" in result:
            resp.update(
                {
                    "otp_id": str(result["otp_id"]),
                    "expires_in": result["expires_in"],
                    "next": "verify_otp",
                }
            )
        else:
            resp.update({"tg_link_token": str(result["tg_link_token"]), "next": "telegram_link"})

        return Response(resp, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth_login"

    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(s.validated_data, status=status.HTTP_200_OK)
