from django.db import models
from django.conf import settings
from django.utils import timezone


class PrivateChatRoom(models.Model):

    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user2')

    connected_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='connected_users')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}."

    def connect_user(self, user):
        is_user_added = False
        if not user in self.connected_users.all():
            self.connected_users.add(user)
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        is_user_removed = False
        if user in self.connected_users.all():
            self.connected_users.remove(user)
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        return f"private-room-{self.id}"


class RoomChatMessageManager(models.Manager):

    def by_room(self, room):
        qs = ChatMessage.objects.filter(room=room).order_by('-timestamp')
        return qs


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone)
    content = models.TextField(blank=False, unique=False)

    objects = RoomChatMessageManager()

    def __str__(self):
        return self.content
