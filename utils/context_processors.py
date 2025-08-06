from django.urls import reverse
from django.conf import settings

def menu_context(request):
    menu = [
        {'title': 'Главная', 'url': reverse('core:home')},
        {'title': 'Пользователи', 'url': reverse('accounts:user_list')},
        {'title': 'Лента', 'url': reverse('social:post_list')},
    ]

    if request.user.is_authenticated:
        menu.append({
            'title': f'Профиль ({request.user.username})',
            'submenu': [
                {'title': 'Профиль', 'url': reverse('accounts:profile')},
                {'title': 'Редактировать', 'url': reverse('accounts:profile_edit')},
                {'title': 'Сменить пароль', 'url': reverse('accounts:password_change')},
                {'title': 'Выход', 'url': reverse('accounts:logout')},
            ]
        })
    else:
        menu.append({
            'title': 'Войти',
            'submenu': [
                {'title': 'Вход', 'url': reverse('accounts:login')},
                {'title': 'Регистрация', 'url': reverse('accounts:register')},
            ]
        })

    return {'menu_items': menu,'main_title': settings.MAIN_TITLE}
