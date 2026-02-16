from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.serializers.telegram_link import TelegramLinkConfirmSerializer


class TelegramLinkConfirmView(APIView):
    permission_classes = [permissions.AllowAny]  # bot chaqiradi

    def post(self, request):
        s = TelegramLinkConfirmSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        u = s.save()
        return Response({"ok": True, "nickname": u.nickname}, status=status.HTTP_200_OK)
