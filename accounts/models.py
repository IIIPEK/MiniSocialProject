# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.id}/{filename}'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    status_message = models.CharField(max_length=100, blank=True, help_text='Девиз или настроение')
    karma = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    telegram = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    viber = models.CharField(max_length=50, blank=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    is_email_confirmed = models.BooleanField(default=False)
    nickname = models.CharField(max_length=50, unique=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nickname

    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def is_fully_active(self):
        """
        Гибкая проверка, разрешена ли активность:
        - подтверждён email
        - не заблокирован (в будущем можно добавить поле is_banned)
        """
        return self.is_active and self.is_email_confirmed


# views.py
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib import messages

User = get_user_model()

def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_email_confirmed = True
        user.save()
        messages.success(request, 'Email подтвержден. Теперь вы можете пользоваться всеми функциями.')
    else:
        messages.error(request, 'Ссылка подтверждения недействительна или устарела.')

    return redirect('accounts:login')
