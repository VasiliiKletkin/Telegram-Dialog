from django.db import models
import random
from djelethon.models.apps import App
from djelethon.models.sessions import ClientSession
from proxies.models import ProxyServer
from telegram.models import TelegramUser
from telethon.errors import PhoneNumberBannedError
from telegram.models import TelegramUser


class TelegramClient(models.Model):
    is_active = models.BooleanField(default=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    session = models.OneToOneField(ClientSession, on_delete=models.CASCADE)
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

    errors = models.TextField(null=True, blank=True)

    @property
    def is_ready(self):
        return (
            (self.proxy.is_ready and self.is_active and not self.errors)
            if self.proxy
            else False
        )

    def __str__(self):
        return f"{self.user.id} - @{self.user.username} - {self.user.first_name}  {self.user.last_name}"

    def check_obj(self):
        try:
            proxy_server = self.proxy

            if not proxy_server:
                raise Exception("Proxy does not exist")
            proxy_server.check_obj()
            if not proxy_server.is_active:
                raise Exception("Proxy is not active")
            elif not proxy_server.is_ready:
                raise Exception("Proxy is not ready")
            elif proxy_server.errors:
                raise Exception(f"Proxy error:{proxy_server.errors}")

            # update_user(client.user.id)
        except PhoneNumberBannedError as error:
            self.errors = str(error)
            self.is_active = False

        except Exception as error:
            self.errors = str(error)
        else:
            self.errors = None
        finally:
            self.save()

    @classmethod
    def get_random(cls, include_ids=None, exclude_ids=None):
        qs = cls.objects.filter(is_active=True)
        if include_ids:
            qs = qs.filter(id__in=include_ids)
        if exclude_ids:
            qs = qs.exclude(id__in=exclude_ids)
        ids = qs.values_list("id", flat=True)
        return cls.objects.get(id=random.choice(ids))
