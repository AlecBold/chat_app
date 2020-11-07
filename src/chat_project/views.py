from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def socket(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def room(request):
    return render(request, 'room.html', {}) 

def login(request):
    return HttpResponse("TODO: login")

def register(request):
    return HttpResponse("TODO: register")
