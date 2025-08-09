#social/models.py
from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from social.managers import PostManager


def post_image_path(instance, filename):
    return f'posts/user_{instance.author.id}/{filename}'


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to=post_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )
    objects = PostManager()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.author.nickname}"
        # return f'{self.author.username}: {self.content[:30]}...'

    def get_absolute_url(self):
        return f'/{self.id}/'

    def comments_count(self):
        return self.comments.count()

    def likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Комментарий от {self.author or 'Аноним'} к посту {self.post_id}"

    def get_absolute_url(self):
        return f'/{self.post_id}/#comment-{self.id}'

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Лайк'),
        ('comment', 'Комментарий'),
        ('follow', 'Подписка'),
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
    verb = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
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

