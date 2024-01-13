"""
Database model for Core
"""

import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
import jwt
from core.manager import UserManager
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {
    'facebook': 'facebook',
    'google': 'google',
    'twitter': 'twitter',
    'email': 'email'
}

class User(AbstractBaseUser, PermissionsMixin):
    """
    Abstract Base User
    - An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    - username, email and password are required. Other fields are optional.

    ### Permissions Mixin
    - Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """

    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Administrator')
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("Username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 10 characters or fewer"
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that staff ID already exists."),
        })
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        }
    )
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    other_name = models.CharField(_("Other Name"), max_length=100, blank=True)
    user_type = models.CharField(_("User Type"), max_length=15, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(
        _("active"),
        db_default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("Staff Status"),
        db_default=False,
        help_text=_("Designates whether the user can log into this admin site.")
    )
    is_verified = models.BooleanField(db_default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        db_default=AUTH_PROVIDERS.get('email')
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "user_type"]

    def __str__(self) -> str:
        return f'{self.username} - {self.name}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        ordering = ["-id"]

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Reset(models.Model):
    email = models.EmailField(
        _("email address"),
        error_messages={
            "unique": _("A user with that email already exists."),
        }
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        error_messages={
            "unique": _("A refresh token already exists."),
        }
    )
