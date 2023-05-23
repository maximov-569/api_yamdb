from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class User(AbstractUser):
    """
    Add two new fields:
    bio - additional info about user
    role - one three permission type roles
    """
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

    @property
    def is_moder(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.Role.ADMINISTRATOR

    class Meta:
        ordering = ['id']
