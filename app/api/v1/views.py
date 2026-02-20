from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.services import UserService

from .serializers import UserSerializer


class UserView(APIView):
    def get(self, request):
        users = UserService.get_all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
