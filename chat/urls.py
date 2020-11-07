from django.urls import path

from .views import create_or_return_chat, chat_room

app_name = 'chat'

urlpatterns = [
    path('create_or_return_chat/', create_or_return_chat, name='create-or-return-chat'),
    path('', chat_room, name='chat-room'),
]
