import hashlib
import hmac
import random
import secrets
import string

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management import call_command

from app.models import IPBlocklist, Passcode


# TODO: Move generic methods into base class
class UserService:
    _User = get_user_model()

    @staticmethod
    def get_all():
        return UserService._User.objects.all()

    @staticmethod
    def get_by_id(user_id: int) -> _User:
        try:
            return UserService._User.objects.get(pk=user_id)
        except UserService._User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

    @staticmethod
    def get_by_username(username: str) -> _User:
        try:
            return UserService._User.objects.get(username=username)
        except UserService._User.DoesNotExist as exc:
            raise ObjectDoesNotExist(
                f"User with username '{username}' does not exist."
            ) from exc

    @staticmethod
    def register(username: str, email: str, password: str, **fields) -> _User:
        try:
            validate_password(password)
        except ValidationError as exc:
            raise exc

        user = UserService._User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **fields,
        )
        user.groups.add(Group.objects.get(name="Bronze"))

        return user

    @staticmethod
    def update(user_id: int, **fields) -> _User:
        try:
            user = UserService._User.objects.get(pk=user_id)
        except UserService._User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

        fields.pop("password", None)

        for attr, value in fields.items():
            setattr(user, attr, value)

        user.save()
        return user

    @staticmethod
    def delete(user_id: int) -> None:
        try:
            user = UserService._User.objects.get(pk=user_id)
        except UserService._User.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist.") from exc

        user.delete()

    @staticmethod
    def assign_new_inquisitor() -> None:
        queryset = UserService._User.objects.exclude(is_inquisitor=True)
        user_count = queryset.count()

        if user_count > 0:
            random_index = random.randrange(user_count)
        else:
            raise ObjectDoesNotExist(
                "No eligible users for becoming a new inquisitor found."
            )

        UserService._User.objects.filter(is_inquisitor=True).update(is_inquisitor=False)

        new_inquisitor = queryset[random_index]
        new_inquisitor.is_inquisitor = True
        new_inquisitor.save()


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


class PasscodeService:
    @staticmethod
    def generate_plain() -> str:
        """Generate a new plain passcode without saving it in the database."""
        alphabet = string.ascii_letters + string.digits + "$&%+-*"
        plain_passcode = "".join(secrets.choice(alphabet) for i in range(25))

        return plain_passcode

    @staticmethod
    def check(passcode: str) -> bool:
        """Compare the passcode to the hash in the database."""
        hashed_passcode = Passcode.objects.first()
        if hashed_passcode is None:
            raise ObjectDoesNotExist("Passcode is absent in the database.")

        return check_password(passcode, hashed_passcode.passcode)

    @staticmethod
    def update(plain_passcode: str) -> None:
        """Hash the passcode and save it in the database."""
        old_passcode = Passcode.objects.first()
        if old_passcode is None:
            old_passcode = Passcode()

        old_passcode.passcode = make_password(plain_passcode)
        old_passcode.save()


# pylint: disable=R0903
class DatabaseService:
    @staticmethod
    def delete_all_data() -> None:
        # Revert migrations
        call_command("migrate", "auth", "zero")

        # Reapply migrations
        call_command("migrate")


class EmailService:
    @staticmethod
    def send_passcode_email(
        to_email: str,
        passcode: str,
        valid_until: str | None = None,
    ) -> None:
        """Send generated passcode via EmailMicroservice."""

        url = settings.EMAIL_SERVICE_BASE_URL + "/send-passcode"

        payload = {
            "to_email": to_email,
            "passcode": passcode,
            "valid_until": valid_until,
        }

        response = requests.post(url, json=payload, timeout=5)

        response.raise_for_status()
