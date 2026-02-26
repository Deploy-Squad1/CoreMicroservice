from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTStatelessUserAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token.encode())
            user = self.get_user(validated_token)
        except AuthenticationFailed as exc:
            raise exc

        return user, validated_token


class IsInGroup(permissions.BasePermission):
    message = "User doesn't have a necessary role."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.auth.payload["role"] in view.required_groups
        )
