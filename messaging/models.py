from django.conf import settings
from django.db import models


class Thread(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="threads"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        users = ", ".join(self.participants.values_list("username", flat=True))
        return f"Чат: {users}"


class Message(models.Model):
    thread = models.ForeignKey(Thread, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Сообщение от {self.sender} в {self.thread}"