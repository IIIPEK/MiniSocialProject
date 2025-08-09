from django.db import models
from django.db.models import Count


class PostQuerySet(models.QuerySet):
    def with_counts(self):
        """Добавляет likes_count и comments_count ко всем Post"""
        return self.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )

class PostManager(models.Manager):
    def get_queryset(self):
        # По умолчанию все запросы включают counts
        return PostQuerySet(self.model, using=self._db).with_counts()

    def with_counts(self):
        # Если нужно явно вызывать
        return self.get_queryset()
