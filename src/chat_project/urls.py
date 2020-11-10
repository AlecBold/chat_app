"""chat_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name="home"),

    path('room/<str:room_id>', views.room_view, name="room"),
    path('rooms/', views.rooms_view, name="rooms"),

    path('join_chat/user/<str:username>', views.join_chat_view, name='join_chat'),

    path('search/', views.search_user_view, name="search"),

    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),

    path('admin/', admin.site.urls, name="admin"),
]
