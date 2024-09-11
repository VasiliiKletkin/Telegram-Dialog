from .base import BaseClientUser, BaseClientUserManager
from django.db import models


class ListenerUserManager(BaseClientUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(client__is_listener=True)


class ActiveListenerUserManager(ListenerUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(client__is_listener=True)


class ListenerUser(BaseClientUser):
    objects = ListenerUserManager()
    active = ActiveListenerUserManager()

    def get_participants(self, chat_id, limit=1000):
        return self.get_client().get_participants(chat_id=chat_id, limit=limit)

    def get_messages(self, chat_id, limit=1000):
        return self.get_client().get_messages(chat_id=chat_id, limit=limit)

    def get_dialogs(self):
        return self.get_client().get_dialogs()

    def save_dialogs(self):
        from telegram_groups.models.groups import TelegramGroup

        for dialog in self.get_dialogs():
            if hasattr(dialog.entity, "title"):
                group, created = TelegramGroup.objects.get_or_create(
                    id=dialog.entity.id,
                    name=dialog.entity.title,
                    groupname=dialog.entity.username,
                )

    class Meta:
        proxy = True
