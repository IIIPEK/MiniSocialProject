from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_verified', 'karma')
    list_filter = ('is_active', 'is_staff', 'is_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name')
