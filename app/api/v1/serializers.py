from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"write_only": True},
        }
