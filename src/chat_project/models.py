from django.db import models

class User(models.Model):
    username = models.CharField(name='username', max_length=255)
    email = models.EmailField(name='email', max_length=255)
    pass

class Room(models.Model):
    pass