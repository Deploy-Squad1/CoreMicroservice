import hashlib
import hmac

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from app.models import IPBlocklist

User = get_user_model()


# TODO: Move generic methods into base class
class UserService:
    @staticmethod
    def get_all():
        return User.objects.all()

    @staticmethod
    def get_by_id(user_id: int) -> User:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

    @staticmethod
    def get_by_username(username: str) -> User:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise ObjectDoesNotExist(
                f"User with username '{username}' does not exist."
            ) from exc

    @staticmethod
    def register(username: str, email: str, password: str, **fields) -> User:
        try:
            validate_password(password)
        except ValidationError as exc:
            raise exc

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **fields,
        )
        return user

    @staticmethod
    def update(user_id: int, **fields) -> User:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

        fields.pop("password", None)

        for attr, value in fields.items():
            setattr(user, attr, value)

        user.save()
        return user

    @staticmethod
    def delete(user_id: int) -> None:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

        user.delete()


class IPBlocklistService:
    @staticmethod
    def hash(ip_address: str) -> str:
        secret_key = settings.SECRET_KEY.encode()
        ip_address = ip_address.encode()

        return hmac.new(secret_key, ip_address, hashlib.sha256).hexdigest()

    @staticmethod
    def add_to_blocklist(ip_address: str) -> None:
        ip_hash = IPBlocklist(ip_address=IPBlocklistService.hash(ip_address))
        try:
            ip_hash.validate_unique()
        except ValidationError as exc:
            raise exc
        ip_hash.save()

    @staticmethod
    def is_blocked(ip_address: str) -> bool:
        ip_hash = IPBlocklistService.hash(ip_address)
        return IPBlocklist.objects.filter(ip_address=ip_hash).exists()
