from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

from .forms import LoginForm, RegisterForm
from .models import User


def register_user(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.username}.")

    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("form is valid")
            form.save()
            print("form is save")
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            print(f"authenticated {account}")
            login(request, account)
            destination = get_redirect_if_exist(request)
            if destination:
                print(f"redirect to {destination}")
                return redirect(destination)
            print("redirect to home")
            return redirect('home')
        else:
            print("form is not valid")
            context['form'] = form
    else:
        print('put form')
        context['form'] = RegisterForm()

    print("get register form")
    return render(request, 'account/register.html', context)


def login_user(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exist(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['form'] = form
    else:
        context['form'] = LoginForm()
    return render(request, 'account/login.html', context)


def get_redirect_if_exist(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect


def logout_user(request):
    logout(request)
    return redirect("home")


def user_search(request, *args, **kwargs):
    context = {}

    if request.method == "GET":
        search_query = request.GET.get('q')
        if len(search_query) > 0:
            search_result = User.objects.filter(username__icontains=search_query)
            context['users'] = search_result

    return render(request, "account/search_result.html", context)
