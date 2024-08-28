from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjTelethonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "djelethon"
    verbose_name = _("Djelethon")
    verbose_name_plural = _("Djelethon")

    def ready(self):
        pass
