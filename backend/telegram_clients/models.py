from django.db import models
import random
from djelethon.models.apps import App
from djelethon.models.sessions import ClientSession
from proxies.models import ProxyServer
from telegram.models import TelegramUser


class TelegramClient(models.Model):
    is_active = models.BooleanField(default=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    session = models.OneToOneField(ClientSession, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    two_fa = models.CharField(max_length=30)
    user = models.OneToOneField(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="client",
    )
    proxy = models.OneToOneField(
        ProxyServer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="client",
    )

    error = models.TextField(null=True, blank=True)

    @property
    def is_ready(self):
        return (
            (self.proxy.is_ready and self.is_active and not self.error)
            if self.proxy
            else False
        )

    def __str__(self):
        return f"{self.user.id} - @{self.user.username} - {self.user.first_name}  {self.user.last_name}"

    @classmethod
    def get_random(cls, include_ids=None, exclude_ids=None):
        qs = cls.objects.filter(is_active=True)
        if include_ids:
            qs = qs.filter(id__in=include_ids)
        if exclude_ids:
            qs = qs.exclude(id__in=exclude_ids)
        ids = qs.values_list("id", flat=True)
        return cls.objects.get(id=random.choice(ids))
