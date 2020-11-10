from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4
from datetime import datetime


def get_id():
    return str(uuid4())


class UserModel(User):
    pass


class RoomModel(models.Model):
    room_id = models.CharField(primary_key=True, unique=True, default=uuid4, max_length=36)
    user1 = models.ForeignKey(UserModel, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserModel, related_name='user2', on_delete=models.CASCADE)


class MessageRoomModel(models.Model):
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, verbose_name='user', on_delete=models.CASCADE)
    message = models.CharField(verbose_name='message', max_length=500)
    date_created = models.DateTimeField(default=datetime.now)


