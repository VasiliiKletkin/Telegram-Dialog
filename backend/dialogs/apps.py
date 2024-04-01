from django.apps import AppConfig


class DialogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dialogs"

    def ready(self):
        from . import tasks, signals
