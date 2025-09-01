from datetime import datetime
from django.urls import reverse
from django.conf import settings

from utils.templatetags.rights import has_any_right
from accounts.models import UserDepartmentRight


def menu_context(request):
    menu = [
        {'title': 'Главная', 'url': reverse('core:home')},
    ]
    social_submenu = [
        {'title': 'Пользователи', 'url': reverse('accounts:user_list')},
        {'title': 'Лента', 'url': reverse('social:post_list')},
    ]
    if request.user.is_authenticated:
        social_submenu.append({'title': 'Мессенджер', 'url': reverse('messaging:thread_list')})
        social_submenu.append({'title': 'Оповещения', 'url': reverse('notifications:notification_list')})


    menu.append({
        'title': f'Общение с коллегами',
        'submenu': social_submenu
    })

    # user_depts = UserDepartmentRight.objects.filter(user=request.user).values_list('department__code', flat=True).distinct()
    # print(list(user_depts),request.user.username)
    if has_any_right(request.user):
        menu.append({'title': 'Заявки', 'url': reverse('requests:request_list')})

    if request.user.is_authenticated:
        # menu.append({'title': 'Мессенджер', 'url': reverse('messaging:thread_list')})
        profile_submenu = [
            {'title': 'Профиль', 'url': reverse('accounts:profile')},
            {'title': 'Редактировать', 'url': reverse('accounts:profile_edit')},
            {'title': 'Сменить пароль', 'url': reverse('accounts:password_change')},
            {'title': 'Настройки', 'url': reverse('accounts:edit_user_settings')},
        ]

        # 👇 Добавим ссылку на админку для суперпользователей
        if request.user.is_superuser:
            profile_submenu.append({'title': 'Админка', 'url': reverse('admin:index')})

        profile_submenu.append({'title': 'Выход', 'url': reverse('accounts:logout')})

        menu.append({
            'title': f'Профиль ({request.user.nickname})',
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
    print(settings.MAIN_TITLE)

    return {'menu_items': menu, 'main_title': settings.MAIN_TITLE, 'year': datetime.now().year,
            'notification': notification}
