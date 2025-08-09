# utils/notifications.py
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction

from social.models import Notification
def create_notification(actor, recipient, verb, target=None):
    """
    Создает уведомление.

    :param actor: Пользователь, который совершил действие
    :param recipient: Получатель уведомления
    :param verb: Тип действия ('like', 'comment', 'follow')
    :param target: Объект действия (пост, комментарий и т.д.)
    """
    if not recipient or actor == recipient:
        return  # Не уведомляем самого себя
    print(actor, recipient, verb, target)
    content_type = None
    object_id = None
    if target is not None:
        content_type = ContentType.objects.get_for_model(target)
        object_id = getattr(target, 'pk', None)

    if verb == 'like' and content_type and object_id is not None:
        existing = Notification.objects.filter(
            actor=actor,
            recipient=recipient,
            verb='like',
            content_type=content_type,
            object_id=object_id
        ).first()
        if existing:
            # Опция: пометить как непрочитанное и обновить время,
            # чтобы оно снова появилось вверху списка:
            if existing.is_read:
                existing.is_read = False
                existing.created_at = timezone.now()
                existing.save(update_fields=['is_read', 'created_at'])
            return existing  # не создаём новый

        # Создаём новое уведомление
        with transaction.atomic():
            notification = Notification(actor=actor, recipient=recipient, verb=verb)
            if target is not None:
                notification.content_type = content_type
                notification.object_id = object_id
            notification.save()
        return notification