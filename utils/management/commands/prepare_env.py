from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Подготавливает окружение: media, static, logs'

    def handle(self, *args, **options):
        steps = ['prepare_media', 'prepare_static', 'prepare_logs']
        for step in steps:
            self.stdout.write(self.style.MIGRATE_HEADING(f'-- Выполняется: {step}'))
            try:
                call_command(step)
            except CommandError as e:
                self.stderr.write(self.style.ERROR(f'Ошибка при {step}: {e}'))
