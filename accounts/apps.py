import os
from django.apps import AppConfig
from django.core.management import call_command

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            try:
                call_command('prepare_env')
            except Exception as e:
                print(f'[startup] Не удалось выполнить prepare_media: {e}')
