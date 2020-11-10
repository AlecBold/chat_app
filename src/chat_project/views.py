from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q

from .forms import RegisterForm, LoginForm
from .models import UserModel, RoomModel, MessageRoomModel


def home_view(request):
    context = {}
    return render(request, 'home.html', context)


def rooms_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        rooms = RoomModel.objects.filter(Q(user1=user) | Q(user2=user))
        rooms_data = []
        for room in rooms:
            d = {}
            if room.user1.username == user.username:
                d['username'] = room.user2.username
            else:
                d['username'] = room.user1.username
            d['room_id'] = room.room_id
            rooms_data.append(d)
        context['rooms'] = rooms_data
        return render(request, 'rooms.html', context)

    return redirect('home')


def room_view(request, room_id):
    context = {}
    user = request.user
    if user.is_authenticated:
        room = RoomModel.objects.get(room_id=room_id)
        if room is not None:
            message_objs = MessageRoomModel.objects.filter(room_id=room_id).order_by('date_created')
            data = []
            for message_obj in message_objs:
                d = {}
                if message_obj.user.username == user.username:
                    d['type'] = 'to'
                else:
                    d['type'] = 'from'
                d['message'] = message_obj.message
                data.append(d)

            context['data'] = data
            context['room_id'] = room_id
            return render(request, 'room.html', context)
        else:
            return HttpResponse("Room does not exist.")

    return redirect('home')


def get_messages(room_id, user):
    context = {}
    room = RoomModel.objects.get(room_id=room_id)
    if room is not None:
        message_objs = MessageRoomModel.objects.filter(room_id=room_id)
        data = []
        for message_obj in message_objs:
            d = {}
            if message_obj.user is user:
                d['type'] = 'from'
            else:
                d['type'] = 'to'
            d['message'] = message_obj.message
            data.append(d)

        context['data'] = data


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            error = "Please enter correct username and password."
            context['errors'] = error
    return render(request, 'login.html', context)


def register_view(request):
    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            context['errors'] = form.errors
    return render(request, 'register.html', context)


def search_user_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            query = request.POST.get("q")
            users = UserModel.objects.filter(Q(username__icontains=query), ~Q(username=user.username))
            context['users'] = users
        else:
            users = UserModel.objects.filter(~Q(username=user.username))
            context['users'] = users
    else:
        return redirect('home')

    return render(request, 'search.html', context)


def join_chat_view(request, username):
    user = request.user
    if user.is_authenticated:
        user_join = UserModel.objects.get(username=username)
        if user_join is None:
            return HttpResponse("User does not exist.")
        elif user == user_join:
            return HttpResponse("You cant join chat with yourself.")
        else:
            try:
                room = RoomModel.objects.get(user1=user, user2=user_join)
            except RoomModel.DoesNotExist:
                try:
                    room = RoomModel.objects.get(user1=user_join, user2=user)
                except RoomModel.DoesNotExist:
                    room = RoomModel(user1=UserModel.objects.get(username=user.username), user2=user_join)
                    room.save()
            print(f"ROOM_ID: {room.room_id}")
            return redirect(f'/room/{room.room_id}')

    return redirect('home')
