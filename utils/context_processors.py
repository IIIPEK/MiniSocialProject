from datetime import datetime
from django.urls import reverse
from django.conf import settings


def menu_context(request):
    menu = [
        {'title': 'Главная', 'url': reverse('core:home')},
        {'title': 'Пользователи', 'url': reverse('accounts:user_list')},
        {'title': 'Лента', 'url': reverse('social:post_list')},
    ]

    if request.user.is_authenticated:
        profile_submenu = [
            {'title': 'Профиль', 'url': reverse('accounts:profile')},
            {'title': 'Редактировать', 'url': reverse('accounts:profile_edit')},
            {'title': 'Сменить пароль', 'url': reverse('accounts:password_change')},
        ]

        # 👇 Добавим ссылку на админку для суперпользователей
        if request.user.is_superuser:
            profile_submenu.append({'title': 'Админка', 'url': reverse('admin:index')})

        profile_submenu.append({'title': 'Выход', 'url': reverse('accounts:logout')})

        menu.append({
            'title': f'Профиль ({request.user.username})',
            'submenu': profile_submenu
        })

    else:
        menu.append({
            'title': 'Войти',
            'submenu': [
                {'title': 'Вход', 'url': reverse('accounts:login')},
                {'title': 'Регистрация', 'url': reverse('accounts:register')},
            ]
        })
    notification = {'link': reverse('notifications:notification_list'), 'unread': 0}
    if request.user.is_authenticated and hasattr(request.user, 'notifications'):
        try:
            notification['unread'] = request.user.notifications.filter(is_read=False).count()
        except Exception:
            notification['unread'] = 0
    return {'menu_items': menu,'main_title': settings.MAIN_TITLE,'year': datetime.now().year, 'notification': notification}
