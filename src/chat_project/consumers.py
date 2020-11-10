import json
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


from .models import UserModel, RoomModel, MessageRoomModel


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f'chat_{self.room_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_id,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_id,
            self.channel_name
        )
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
                'from': user.username
            }
        )

        message_obj = MessageRoomModel(
            user=UserModel.objects.get(username=user),
            room=RoomModel.objects.get(room_id=self.room_id),
            message=message
        )
        message_obj.save()

    def chat_message(self, event):
        data = {
            'type': 'to' if self.scope['user'].username == event['from'] else 'from',
            'message': event["message"]
        }
        self.send(text_data=json.dumps(data))

