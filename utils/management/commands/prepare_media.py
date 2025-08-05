import os
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Создает каталог media/ при необходимости'

    def handle(self, *args, **options):
        media_path = settings.MEDIA_ROOT
        try:
            os.makedirs(media_path, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f'Каталог media создан или уже существует: {media_path}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при создании media: {e}'))
