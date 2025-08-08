# utils/notifications.py
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

from social.models import Notification
def create_notification(actor, recipient, verb, target=None):
    """
    Создает уведомление.

    :param actor: Пользователь, который совершил действие
    :param recipient: Получатель уведомления
    :param verb: Тип действия ('like', 'comment', 'follow')
    :param target: Объект действия (пост, комментарий и т.д.)
    """
    if actor == recipient:
        return  # Не уведомляем самого себя
    print(actor, recipient, verb, target)
    try:
        notification = Notification(actor=actor, recipient=recipient, verb=verb)
        if target:
            notification.content_type = ContentType.objects.get_for_model(target)
            notification.object_id = target.pk
        notification.save()
    except IntegrityError:
        # логирование
        pass
    except Exception as e:
        # логирование ошибки
        pass