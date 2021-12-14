from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def create_superuser(
            self,
            email,
            username,
            first_name=None,
            last_name=None,
            password=None
    ):
        user = self.create_user(
            email=email,
            username=username,
            is_staff=True,
            is_superuser=True,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True, blank=True)
