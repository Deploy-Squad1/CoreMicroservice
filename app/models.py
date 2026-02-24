from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )


class Passcode(models.Model):
    """
    Model that represents a daily updated passcode for accessing
    the website.
    """

    passcode = models.CharField(_("password"), max_length=128)
