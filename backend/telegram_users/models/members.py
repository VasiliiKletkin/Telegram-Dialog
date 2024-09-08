from .users import TelegramUser
from django.db import models


class MemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(client__isnull=True)


class MemberUser(TelegramUser):
    objects = MemberManager()

    class Meta:
        proxy = True
