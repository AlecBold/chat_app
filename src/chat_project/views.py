from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate

from .forms import RegisterForm, LoginForm


def index(request):
    context = {}
    return render(request, 'home.html', context)


def rooms(request):
    context = {}
    return render(request, 'rooms.html', context)


def room(request):
    context = {}
    return render(request, 'room.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            error = "Please enter correct username and password."
            context['errors'] = form.error_messages
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
