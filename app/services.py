import secrets
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from app.models import Passcode


# TODO: Move generic methods into base class
class UserService:
    User = get_user_model()

    @staticmethod
    def get_all():
        return UserService.User.objects.all()

    @staticmethod
    def get_by_id(user_id: int) -> User:
        try:
            return UserService.User.objects.get(pk=user_id)
        except UserService.User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

    @staticmethod
    def get_by_username(username: str) -> User:
        try:
            return UserService.User.objects.get(username=username)
        except UserService.User.DoesNotExist as exc:
            raise ObjectDoesNotExist(
                f"User with username '{username}' does not exist."
            ) from exc

    @staticmethod
    def register(username: str, email: str, password: str, **fields) -> User:
        try:
            validate_password(password)
        except ValidationError as exc:
            raise exc

        user = UserService.User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **fields,
        )
        return user

    @staticmethod
    def update(user_id: int, **fields) -> User:
        try:
            user = UserService.User.objects.get(pk=user_id)
        except UserService.User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

        fields.pop("password", None)

        for attr, value in fields.items():
            setattr(user, attr, value)

        user.save()
        return user

    @staticmethod
    def delete(user_id: int) -> None:
        try:
            user = UserService.User.objects.get(pk=user_id)
        except UserService.User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

        user.delete()


class PasscodeService:
    @staticmethod
    def generate_new() -> str:
        old_passcode = Passcode.objects.first()
        if old_passcode is None:
            old_passcode = Passcode()

        # Generating new passcode randomly
        alphabet = string.ascii_letters + string.digits + "$&%+-*{}()[]"
        new_plain_passcode = "".join(secrets.choice(alphabet) for i in range(25))

        old_passcode.passcode = make_password(new_plain_passcode)
        old_passcode.save()

        return new_plain_passcode

    @staticmethod
    def check_passcode(passcode: str) -> bool:
        hashed_passcode = Passcode.objects.first()
        if hashed_passcode is None:
            raise ObjectDoesNotExist("Passcode is absent in the database.")

        return check_password(passcode, hashed_passcode.passcode)
