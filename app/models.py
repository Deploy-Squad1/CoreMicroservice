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


class IPBlocklist(models.Model):
    ip_address = models.CharField(
        _("ip hash"),
        unique=True,
        max_length=128,
        error_messages={
            "unique": _("This IP is already blocked."),
        },
    )


class Passcode(models.Model):
    """
    Model that represents a daily updated passcode for accessing
    the website.
    """

    passcode = models.CharField(_("passcode"), max_length=128)
