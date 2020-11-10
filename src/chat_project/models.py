from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class UserModel(User):
    pass


class RoomModel(models.Model):
    room_id = models.CharField(primary_key=True, auto_created=True, max_length=50)
    user1 = models.ForeignKey(UserModel, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserModel, related_name='user2', on_delete=models.CASCADE)


class MessageRoomModel(models.Model):
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, verbose_name='user', on_delete=models.CASCADE)
    message = models.CharField(verbose_name='message', max_length=500)
    date_created = models.DateTimeField(default=datetime.now)


