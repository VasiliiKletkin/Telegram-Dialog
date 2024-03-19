from django.db import models
from django_telethon.models import App, ClientSession
from model_utils.models import TimeStampedModel
from proxies.models import ProxyServer


class TelegramGroup(TimeStampedModel):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - @{self.username}"


class TelegramGroupMessage(models.Model):
    group = models.ForeignKey(
        TelegramGroup, on_delete=models.CASCADE)
    message_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    reply_to_msg_id = models.BigIntegerField()
    message = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.group} - {self.message}"


class TelegramUser(TimeStampedModel):
    is_active = models.BooleanField(default=False)

    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(
        default="", max_length=64, null=True, blank=True)
    last_name = models.CharField(
        default="", max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    two_fa = models.CharField(max_length=30, null=True, blank=True)

    app = models.OneToOneField(
        App, on_delete=models.CASCADE)
    client_session = models.OneToOneField(
        ClientSession, on_delete=models.CASCADE)

    proxy_server = models.OneToOneField(
        ProxyServer, on_delete=models.SET_NULL, null=True, blank=True, related_name="telegram_user")

    app_json = models.JSONField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - @{self.username} - {self.first_name}  {self.last_name}"

    @property
    def is_ready(self):
        return (self.proxy_server.is_ready and self.is_active) if self.proxy_server else False
