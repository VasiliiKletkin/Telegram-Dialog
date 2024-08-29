from django.db import models

from djelethon.models.apps import App
from djelethon.models.sessions import ClientSession
from proxies.models import ProxyServer
from telegram.models import TelegramUser


class TelegramClient(models.Model):
    is_active = models.BooleanField(default=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE, null=True)
    session = models.OneToOneField(ClientSession, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=30)
    two_fa = models.CharField(max_length=30)
    telegram_user = models.OneToOneField(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="telegram_client",
    )
    proxy_server = models.OneToOneField(
        ProxyServer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="telegram_client",
    )

    error = models.TextField(null=True, blank=True)

    @property
    def is_ready(self):
        return (
            (self.proxy_server.is_ready and self.is_active and not self.error)
            if self.proxy_server
            else False
        )

    def __str__(self):
        return f"{self.telegram_user.id} - @{self.telegram_user.username} - {self.telegram_user.first_name}  {self.telegram_user.last_name}"

    @classmethod
    def get_random(cls, include_ids=None, exclude_ids=None):
        qs = cls.objects.filter(is_active=True)
        if include_ids:
            qs = qs.filter(id__in=include_ids)
        if exclude_ids:
            qs = qs.exclude(id__in=exclude_ids)
        ids = qs.values_list("id", flat=True)
        return cls.objects.get(id=random.choice(ids))
