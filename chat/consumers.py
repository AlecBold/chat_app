from django.utils import timezone
from django.core.paginator import Paginator
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json
import asyncio

from account.models import User
from account.exceptions import LazyUserEncoder
from .exceptions import ClientError
from .models import PrivateChatRoom, ChatMessage
from .utils import LazyRoomChatMessageEncoder


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['broadcast']

    async def connect(self):
        await self.accept()
        self.room_id = None

    async def receive_json(self, content):
        command = content.get('command', None)
        try:
            if command == 'join':
                await self.join_room(content['room'])

            elif command == 'leave':
                await self.leave_room(content['room'])

            elif command == 'send':
                if len(content['message'].lstrip()) == 0:
                    raise ClientError(422 , "You can't send an empty message.")
                await self.send_room(content['room'], content['message'])

            elif command == "get_room_chat_messages":
                room = await get_room_or_error(content['room_id'], self.scope['user'])
                payload = await get_room_chat_messages(room, content['page_number'])
                if payload == None:
                    payload = json.loads(payload)
                    await self.send_messages_payload(payload['messages'], payload['new_page_number'])
                else:
                    raise ClientError(204, "Something went wrong retrieving the chatroom messages.")

            elif command == "get_user_info":
                room = await get_room_or_error(content['room_id'], self.scope['user'])
                payload = get_user_info(room, self.scope['user'])
                if payload != None:
                    payload = json.loads(payload)
                    await self.send_user_info_payload(payload['user_info'])
                else:
                    raise ClientError(204, "Something went wrong retrieving the chatroom messages.")

        except ClientError as e:
            error_data = {}
            error_data['error'] = e.code
            if e.message:
                error_data['message'] == e.message
            await self.send_json(error_data)

    async def disconnect(self, code):
        try:
            if self.room_id != None:
                await self.leave_room(self.room_id)
        except Exception as e:
            print(f"Exception: {str(e)}")
            pass

    async def join_room(self, room_id):
        try:
            room = await get_room_or_error(room_id, self.scope['user'])
        except ClientError as e:
            error_data = {}
            error_data['error'] = e.message
            await self.send_json(error_data)
            return

        await connect_user(room, self.scope['user'])

        self.room_id = room_id

        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )

        await self.send_json({
            'join': str(room_id),
            'username': self.scope['user'].username,
        })

        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    'type': 'chat.join',
                    'room_id': room_id,
                    'username': self.scope['user'].username
                }
            )

    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        print("ChatConsumer: leave_room")
        room = await get_room_or_error(room_id, self.scope["user"])

        # Remove user from "connected_users" list
        await disconnect_user(room, self.scope["user"])

        # Notify the group that someone left
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.leave",
                "room_id": room_id,
                "username": self.scope["user"].username,
            }
        )

        # Remove that we're in the room
        self.room_id = None

        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send_json({
            "leave": str(room.id),
        })

    async def chat_join(self, event):
        if event['username']:
            await self.send_json(
                {
                    'room': event['room_id'],
                    'username': event['username'],
                    'message': event['username'] + ' joined chat.'
                }
            )

    async def chat_leave(self, event):
        if event['username']:
            await self.send_json(
                {
                    'room': event['room_id'],
                    'username': event['username'],
                    'message': event['username'] + ' leaved chat.',
                }
            )

    async def chat_message(self, event):
        timestamp = str(timezone.now())
        await self.send_json(
            {
                "username": event['username'],
                "message": event['message'],
                "timestamp": timestamp,
            },
        )


@database_sync_to_async
def create_room_chat_message(room, user, message):
    return ChatMessage.objects.create(user=user, room=room, content=message)


@database_sync_to_async
def connect_user(room, user):
    # add user to connected_users list
    account = User.objects.get(username=user.username)
    return room.connect_user(account)


@database_sync_to_async
def disconnect_user(room, user):
    # remove from connected_users list
    account = User.objects.get(username=user.username)
    return room.disconnect_user(account)


@database_sync_to_async
def get_room_or_error(room_id, user):
    try:
        room = PrivateChatRoom.objects.get(pk=room_id)
    except PrivateChatRoom.DoesNotExist:
        raise ClientError("ROOM_INVALID", "Invalid room.")

    if user != room.user1 and user != room.user2:
        raise ClientError("ROOM_ACCESS_DENIED", "Access denied.")

    return room


@database_sync_to_async
def get_room_chat_messages(room, page_number):
    try:
        qs = ChatMessage.objects.by_room(room)
        p = Paginator(qs, 50)

        payload = {}
        message_data = None
        new_page_number = int(page_number)
        if new_page_number <= p.num_pages:
            new_page_number += 1
            s = LazyRoomChatMessageEncoder()
            payload['messages'] = s.serialize(p.page(page_number).object_list)
        else:
            payload['messages'] = "None"
        payload['new_page_number'] = new_page_number
        return json.dumps(payload)
    except Exception as e:
        print(f"Exception: {str(e)}")
        return None


def get_user_info(room, user):
    try:
        other_user = room.user1
        if other_user == user:
            other_user = room.user2

        payload = {}
        s = LazyUserEncoder()
        payload['user_info'] = s.serialize([other_user])[0]
        return json.dumps(payload)
    except Exception as e:
        print(f"Exception: {str(e)}")
        return None
