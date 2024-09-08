from telegram.models import TelegramUser
from django.db import models


class ActorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(client__isnull=True)


class MemberUser(TelegramUser):
    objects = ActorManager()

    class Meta:
        proxy = True
