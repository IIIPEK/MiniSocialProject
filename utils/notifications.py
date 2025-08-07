from social.models import Notification
from django.contrib.contenttypes.models import ContentType

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
    notification = Notification(
        actor=actor,
        recipient=recipient,
        verb=verb
    )

    if target:
        notification.content_type = ContentType.objects.get_for_model(target)
        notification.object_id = target.id

    notification.save()