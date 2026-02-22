from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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
    def register(username: str, password: str, **fields) -> User:
        try:
            validate_password(password)
        except ValidationError as exc:
            raise exc

        user = User.objects.create_user(
            username=username,
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
