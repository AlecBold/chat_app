from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class AccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have email.")
        if not username:
            raise ValueError("Users must have username.")
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.TextField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# class ChatRoom(models.Model):
#     pass


# class Message(models.Model):
#     chat_room = models.ForeignKey(ChatRoom, related_name='messages')
#     message = models.TextField()
#     timestamp = models.DateTimeField(default=timezone.now(), db_index=True)

