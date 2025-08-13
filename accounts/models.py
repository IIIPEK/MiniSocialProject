# accounts/models.py
from django.conf import settings
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



class UserSetting(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="settings"
    )
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user.username} - {self.name} = {self.value}"
