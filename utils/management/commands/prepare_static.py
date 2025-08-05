import os
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Создаёт каталог STATIC_ROOT'

    def handle(self, *args, **options):
        static_path = settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'staticfiles')
        try:
            os.makedirs(static_path, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f'Каталог static создан или уже существует: {static_path}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при создании static: {e}'))
