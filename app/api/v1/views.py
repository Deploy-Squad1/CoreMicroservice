from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from app.services import IPBlocklistService, UserService

from .serializers import UserSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserService.register(
                serializer.validated_data.get("username"),
                serializer.validated_data.get("email"),
                serializer.validated_data.get("password"),
            )
        except ValidationError as exc:
            return Response(
                {"password": [error.message for error in exc.error_list]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        try:
            user = UserService.get_by_username(request.data.get("username"))
        except ObjectDoesNotExist as exc:
            return Response({"username": exc.args}, status.HTTP_404_NOT_FOUND)

        if not user.check_password(request.data.get("password")):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        serializer = UserSerializer(user)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=str(access_token),
            httponly=True,
            samesite="Lax",
            expires=datetime.fromtimestamp(access_token.payload.get("exp")),
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh_token),
            httponly=True,
            samesite="Lax",
            expires=datetime.fromtimestamp(refresh_token.payload.get("exp")),
        )
        return response


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = RefreshToken(request.COOKIES.get("refresh_token"))
        except TokenError as exc:
            return Response(exc.args, status=status.HTTP_401_UNAUTHORIZED)

        if refresh_token is None:
            return Response(
                {"Refresh token is required"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            UserService.get_by_id(refresh_token.payload.get(api_settings.USER_ID_CLAIM))
        except ObjectDoesNotExist as exc:
            return Response(exc.args, status=status.HTTP_401_UNAUTHORIZED)

        new_access_token = refresh_token.access_token

        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=str(new_access_token),
            httponly=True,
            samesite="Lax",
            expires=datetime.fromtimestamp(new_access_token.payload.get("exp")),
        )
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class AddIPToBlocklistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ip_address = request.data.get("ipAddress")
        if ip_address is None:
            return Response(
                {"ipAddress": ["IP address is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            IPBlocklistService.add_to_blocklist(ip_address)
        except ValidationError as exc:
            return Response(exc.message_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class CheckIPView(APIView):
    def get(self, request):
        ip_address = request.META.get("REMOTE_ADDR")

        if IPBlocklistService.is_blocked(ip_address):
            return Response(
                {"redirect": settings.BLOCKED_IP_REDIRECT_URL},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(status=status.HTTP_200_OK)
