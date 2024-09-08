from telegram.models import TelegramUser
from django.db import models


class ListenerManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                client__isnull=False,
                client__is_active=True,
            )
        )


class ListenerUser(TelegramUser):
    objects = ListenerManager()

    class Meta:
        proxy = True
