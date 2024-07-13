from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=120)
    activation_code = models.CharField(max_length=6, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.fullname()
