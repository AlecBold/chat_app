from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import timezone

from urllib.parse import urlencode
import json
from itertools import chain

from .models import PrivateChatRoom, ChatMessage
from .utils import create_or_get_chat

DEBUG = False


def chat_room(request):
    room_id = request.GET.get('room_id')
    user = request.user
    if not user.id_authenticated:
        base_url = reverse('login')
        query_string = urlencode({'next': f'chat/?room_id={room_id}'})
        url = f'{base_url}?{query_string}'
        return redirect(url)

    context = {}

    if room_id:
        room = PrivateChatRoom.objects.get(pk=room_id)
        context['room'] = room

    context['m_and_f'] = get_recent_chatroom_messages(user)

    context['BASE_URl'] = settings.BASE_URL
    context['debug'] = DEBUG
    context['debug_mode'] = settings.DEBUG
    return render(request, 'chat/room.html', context)


def get_recent_chatroom_messages(user):
    rooms1 = PrivateChatRoom.objects.filter(user1=user, is_active=True)
    rooms2 = PrivateChatRoom.objects.filter(user2=user, is_active=True)

    rooms = list(chain(rooms1, rooms2))

    m_and_f = []
    for room in rooms:
        if room.user1 == user:
            friend = room.user2
        else:
            friend = room.user1

        try:
            message = ChatMessage.objects.filter(room=room, user=friend).latest('timestamp')
        except Exception as e:
            message = ChatMessage(
                user=friend,
                room=room,
                timestamp=str(timezone()),
                content='',
            )
        m_and_f.append({
            'message': message,
            'friend': friend
        })

    return sorted(m_and_f, key=lambda x: x['message'].timestamp, reverse=True)


def create_or_return_chat(request, *args, **kwargs):
    user1 = request.user
    payload = {}
    if user1.is_authenticated:
        if request.method == "POST":
            user2_name = request.POST.get('user2_')