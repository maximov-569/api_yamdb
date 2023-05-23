from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class UserManager(models.Manager):
    pass


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    class Role(models.TextChoices):
        USER = 'user', gettext_lazy("User")
        MODERATOR = 'moderator', gettext_lazy("Moderator")
        ADMINISTRATOR = 'admin', gettext_lazy("Administrator")

    role = models.CharField(
        max_length=9,
        choices=Role.choices,
        default=Role.USER,
    )

    objects = UserManager()
