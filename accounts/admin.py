from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_email_confirmed', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'is_email_confirmed')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': (
                'avatar',
                'bio',
                'status_message',
                'karma',
                'is_verified',
                'location',
                'website',
                'date_of_birth',
                'telegram',
                'whatsapp',
                'viber',
                'following',
                'is_email_confirmed',
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': (
                'avatar',
                'bio',
                'status_message',
                'karma',
                'is_verified',
                'location',
                'website',
                'date_of_birth',
                'telegram',
                'whatsapp',
                'viber',
                'following',
                'is_email_confirmed',
            ),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

# Авто-регистрация остальных моделей
app = apps.get_app_config('accounts')

for model in app.get_models():
    if model != CustomUser:
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            pass
