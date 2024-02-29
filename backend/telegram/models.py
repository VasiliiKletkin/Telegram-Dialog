import time
from django.db import models
from model_utils.models import TimeStampedModel
from django_telethon.models import ClientSession, App
from django_telethon.sessions import DjangoSession

from asgiref.sync import async_to_sync
from telegram.utils import send_message

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

    def send_message(self, chat_id, message):
        sleep_time = 60/150 * len(message)
        time.sleep(sleep_time)
        django_session = DjangoSession(client_session=self.session)
        async_to_sync(send_message)(chat_id, message,
                                    django_session, self.app.api_id, self.app.api_hash, self.proxy_server.get_proxy_dict())


class TelegramUserUpload(models.Model):
    json_field = models.FileField(upload_to='telegram_json')
    session_file = models.FileField(upload_to='telegram_session')

    def __str__(self):
        return f'{self.id}'
