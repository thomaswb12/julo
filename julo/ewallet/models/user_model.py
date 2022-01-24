from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from ..managers import CustomUserManager
from .abstract_model import CommonInfo
import uuid


class CustomUser(AbstractBaseUser, PermissionsMixin, CommonInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = None
    username = None
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.id)

    def get_identity(self):
        return str(self.id)