from django.db import models


class User(models.Model):
    username = models.CharField(name='username', max_length=255)

class Room(models.Model):
    pass