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

    app = models.ForeignKey(
        App, on_delete=models.CASCADE)
    client_session = models.ForeignKey(
        ClientSession, on_delete=models.CASCADE)

    proxy_server = models.ForeignKey(
        ProxyServer, on_delete=models.SET_NULL, null=True, blank=True)

    app_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - @{self.username} - {self.first_name}  {self.last_name}"

    def check_active(self):
        return (self.proxy_server.check_active() and self.is_active) if self.proxy_server else False
