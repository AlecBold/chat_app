from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_admin')
    search_fields = ('username', 'email')
    readonly_fields = ('id', 'date_joined')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
