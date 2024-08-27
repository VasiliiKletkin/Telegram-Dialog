from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjTelethonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dj_telethon'

    verbose_name = _("Django Telethon")
    verbose_name_plural = _("Django Telethon")

    def ready(self):
        from .receivers import receiver_telegram_client_registered  # noqa: F401
