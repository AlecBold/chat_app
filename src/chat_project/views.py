from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def rooms(request):
    return render(request, 'rooms.html', {}) 

def room(request):
    return render(request, 'room.html', {}) 

def login(request):
    return render(request, 'login.html', {}) 

def register(request):
    return render(request, 'register.html', {}) 
