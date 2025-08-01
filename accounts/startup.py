from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def run_prepare_media(sender, **kwargs):
    try:
        call_command('prepare_media')
    except Exception as e:
        print(f'[startup] Не удалось выполнить prepare_media: {e}')
