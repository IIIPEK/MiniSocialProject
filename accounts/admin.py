from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {
            'fields': (
                'avatar', 'birth_date', 'website',
                'telegram', 'whatsapp', 'viber',
                'bio', 'status_message', 'karma'
            ),
        }),
    )

# Авто-регистрация остальных моделей
app = apps.get_app_config('accounts')

for model in app.get_models():
    if model != CustomUser:
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            pass
