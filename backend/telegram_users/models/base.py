from .users import TelegramUser
from django.db import models


class BaseClientUserManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                client__isnull=False,
                client__is_active=True,
            )
        )


class BaseClientUser(TelegramUser):
    objects = BaseClientUserManager()

    class Meta:
        proxy = True

    def get_client(self):
        return self.client

    @property
    def is_ready(self):
        return self.get_client().is_ready

    def is_member(self, group_id):
        return super().is_member(group_id)

    def get_me(self):
        return self.get_client().get_me()

    def check_obj(self):
        return self.get_client().check_obj()

    def join_chat(self, chat_id):
        return self.get_client().join_chat(chat_id)
