from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password", "groups"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"write_only": True},
        }
