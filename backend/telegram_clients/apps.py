from django.apps import AppConfig


class TelegramClientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_clients'

    # def ready(self):
    #     from . import tasks  # noqa