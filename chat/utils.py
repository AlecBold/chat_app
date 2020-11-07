from django.core.serializers.python import Serializer
from django.utils.timezone import timezone

from .models import PrivateChatRoom


def create_or_get_chat(user1, user2):
    try:
        chat = PrivateChatRoom.objects.get(user1=user1, user2=user2)
    except Exception as e:
        try:
            chat = PrivateChatRoom.objects.get(user1=user2, user2=user1)
        except Exception as e:
            chat = PrivateChatRoom(user1=user1, user2=user2)
            chat.save()
    return chat


class LazyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'msg_id': str(obj.id)})
        dump_object.update({'username': str(obj.user.username)})
        dump_object.update({'message': str(obj.content)})
        dump_object.update({'timestamp': str(obj.timestamp)})
        return dump_object
