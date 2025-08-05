import os
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Создаёт каталог logs/'

    def handle(self, *args, **options):
        logs_path = os.path.join(settings.BASE_DIR, 'logs')
        try:
            os.makedirs(logs_path, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f'Каталог logs создан или уже существует: {logs_path}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при создании logs: {e}'))
