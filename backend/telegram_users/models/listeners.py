from .base import BaseClientUser
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


class ListenerUser(BaseClientUser):
    objects = ListenerManager()

    def get_participants(self):
        return self.client.get_participants()

    def get_messages(self, chat_id, limit=1000):
        return self.client.get_messages(chat_id=chat_id, limit=limit)

    def get_dialogs(self):
        return self.client.get_dialogs()

    class Meta:
        proxy = True
