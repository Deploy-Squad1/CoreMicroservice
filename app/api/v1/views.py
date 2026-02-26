from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from app.services import UserService

from .serializers import UserSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserService.register(
                serializer.validated_data["username"],
                serializer.validated_data["email"],
                serializer.validated_data["password"],
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
            user = UserService.get_by_username(request.data["username"])
        except ObjectDoesNotExist as exc:
            return Response({"username": exc.args}, status.HTTP_404_NOT_FOUND)

        if not user.check_password(request.data["password"]):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = RefreshToken.for_user(user)
        refresh_token["role"] = user.groups.first().name
        access_token = refresh_token.access_token

        serializer = UserSerializer(user)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=str(access_token),
            httponly=True,
            samesite="Lax",
            expires=datetime.fromtimestamp(access_token.payload["exp"]),
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh_token),
            httponly=True,
            samesite="Lax",
            expires=datetime.fromtimestamp(refresh_token.payload["exp"]),
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
            user = UserService.get_by_id(
                refresh_token.payload.get(api_settings.USER_ID_CLAIM)
            )
        except ObjectDoesNotExist as exc:
            return Response(exc.args, status=status.HTTP_401_UNAUTHORIZED)

        response = Response(status=status.HTTP_200_OK)

        if refresh_token.payload.get("role") != user.groups.first().name:
            refresh_token = RefreshToken.for_user(user)
            refresh_token["role"] = user.groups.first().name
            response.set_cookie(
                key="refresh_token",
                value=str(refresh_token),
                httponly=True,
                samesite="Lax",
                expires=datetime.fromtimestamp(refresh_token.payload["exp"]),
            )

        new_access_token = refresh_token.access_token

        response.set_cookie(
            key="access_token",
            value=str(new_access_token),
            httponly=True,
            samesite="Lax",
            expires=datetime.fromtimestamp(new_access_token.payload["exp"]),
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
