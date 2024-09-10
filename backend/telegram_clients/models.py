from django.db import models

from django.utils.timezone import now

from .utils import (
    get_dialogs as _get_dialogs,
    join_chat as _join_chat,
    get_me as _get_me,
    send_message as _send_message,
    get_messages as _get_messages,
    get_participants as _get_participants,
)

from djelethon.sessions import DjangoSession
from djelethon.models.apps import App
from djelethon.models.sessions import ClientSession
from proxies.models import ProxyServer
from telegram_users.models import TelegramUser
from telethon.errors import PhoneNumberBannedError


class TelegramClient(models.Model):
    is_active = models.BooleanField(default=False)
    last_check = models.DateTimeField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
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

    @property
    def is_ready(self):
        return (
            (
                self.proxy.is_ready
                and self.is_active
                and not self.errors
                and bool(self.last_check)
            )
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
            self.get_me()
        except PhoneNumberBannedError as error:
            self.errors = str(error)
            self.is_active = False
        except Exception as error:
            self.errors = str(error)
        else:
            self.errors = None
        finally:
            self.last_check = now()
            self.save()

    def get_client_kwargs(self):
        return {
            "session": DjangoSession(self.session),
            "api_id": self.app.api_id,
            "api_hash": self.app.api_hash,
            "proxy": self.proxy.get_proxy_dict(),
        }

    def get_me(self):
        return _get_me(**self.get_client_kwargs())

    def get_dialogs(self):
        return _get_dialogs(**self.get_client_kwargs())

    def get_messages(self, chat_id, limit=1000):
        return _get_messages(
            **self.get_client_kwargs(),
            chat_id=chat_id,
            limit=limit,
        )

    def get_participants(self, chat_id, limit=1000):
        return _get_participants(
            **self.get_client_kwargs(),
            chat_id=chat_id,
            limit=limit,
        )

    def join_chat(self, chat_id):
        return _join_chat(
            **self.get_client_kwargs(),
            chat_id=chat_id,
        )

    def send_message(self, chat_id, text, reply_to_msg_id=None):
        return _send_message(
            **self.get_client_kwargs(),
            chat_id=chat_id,
            text=text,
            reply_to_msg_id=reply_to_msg_id,
        )
