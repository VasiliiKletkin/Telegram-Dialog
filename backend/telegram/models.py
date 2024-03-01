from django.db import models
from django_telethon.models import App, ClientSession
from model_utils.models import TimeStampedModel
from proxies.models import ProxyServer


class TelegramGroup(TimeStampedModel):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - @{self.username}"


class TelegramUser(TimeStampedModel):
    is_active = models.BooleanField(default=True)

    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(
        default="", max_length=64, null=True, blank=True)
    last_name = models.CharField(
        default="", max_length=64, null=True, blank=True)

    app = models.ForeignKey(
        App, on_delete=models.CASCADE)
    session = models.ForeignKey(
        ClientSession, on_delete=models.CASCADE)

    proxy_server = models.ForeignKey(
        ProxyServer, on_delete=models.SET_NULL, null=True, blank=True)

    app_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - @{self.username} - {self.first_name}  {self.last_name}"
