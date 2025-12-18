from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import HeartRate, WearOSIntegration
from .serializers import (
    HeartRateSerializer,
    WearOSAuthSerializer,
    WearOSTokenSerializer,
)


class WearOSAuthView(GenericAPIView):
    """API view for WearOS device authentication and token issuance."""

    serializer_class = WearOSAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if not user:
                return Response(
                    {"detail": "ユーザ名またはパスワードが正しくありません。"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # initialize or update WearOSIntegration
            token = WearOSIntegration.generate_token()
            token_hash = WearOSIntegration.hash_token(token)
            integration, created = WearOSIntegration.objects.get_or_create(user=user)
            integration.token_hash = token_hash
            integration.save()
            return Response({"token": token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HeartRateReceiveView(GenericAPIView):
    """API view for receiving heart rate data from WearOS devices using token authentication."""

    serializer_class = HeartRateSerializer

    def post(self, request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return Response(
                {"error": "認証トークンが必要です。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token = token.replace("Bearer ", "")
        # Validate token and get associated user
        try:
            integration = WearOSIntegration.objects.get(
                token_hash=WearOSIntegration.hash_token(token)
            )
            user = integration.user
        except WearOSIntegration.DoesNotExist:
            return Response(
                {"error": "無効なトークンです。"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bpm = serializer.validated_data["bpm"]
            timestamp = serializer.validated_data["timestamp"]

            HeartRate.objects.create(user=user, bpm=bpm, timestamp=timestamp)
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
