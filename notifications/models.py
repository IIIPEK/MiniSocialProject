# notifications/models.py
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import UniqueConstraint, Q

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Лайк'),
        ('comment', 'Комментарий'),
        ('follow', 'Подписка'),
        # заявки:
        ("request_approved", "Заявка утверждена"),
        ("request_rejected", "Заявка отклонена"),
        ("request_cancelled", "Заявка отменена"),
        ("po_created", "PO создано"),
        ("request_status", "Статус заявки изменён"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actor_notifications'
    )
    verb = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # Для связи с объектом (например, постом или комментарием)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['actor', 'recipient', 'verb', 'content_type', 'object_id'],
                condition=Q(verb='like'),
                name='unique_like_notification'
            ),
        ]

    def __str__(self):
        return f'{self.actor} -> {self.recipient}: {self.verb}'

