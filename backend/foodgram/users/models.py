from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.constraints import CheckConstraint, UniqueConstraint


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
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    email = models.EmailField('email address', unique=True)
    is_active = models.BooleanField(default=True, blank=True)
    username = models.CharField('username', max_length=150, unique=True)

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('username', 'email',),
                name='uniq_user_email'
            ),
        )

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='following'
    )
    objects = models.Manager()

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('author', 'user',),
                name='unique_follow'
            ),
            CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_is_not_following')
        )

    def __str__(self):
        return f'{self.user} follow to {self.author}'
