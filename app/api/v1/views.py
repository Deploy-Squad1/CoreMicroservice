from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app.services import UserService

from .serializers import UserSerializer


class UserView(APIView):
    def get(self, request):
        users = UserService.get_all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserService.create(
                serializer.validated_data["username"],
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
        user = UserService.get_by_username(request.data["username"])
        if not user.check_password(request.data["password"]):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        access_token = RefreshToken.for_user(user).access_token

        serializer = UserSerializer(user)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=str(access_token),
            httponly=True,
            samesite="Lax",
            max_age=access_token.lifetime,
        )
        return response
