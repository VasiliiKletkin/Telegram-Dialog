from django.db import models

from telegram_groups.models.groups import TelegramGroup

from .utils import (
    get_dialogs as _get_dialogs,
    join_chat as _join_chat,
    get_me as _get_me,
    send_message as _send_message,
    get_messages as _get_messages,
    get_participants as _get_participants,
)
from telethon.sync import TelegramClient as Client

from djelethon.sessions import DjangoSession
from djelethon.models.apps import App
from djelethon.models.sessions import ClientSession
from proxies.models import ProxyServer
from telegram_users.models import TelegramUser
from telethon.errors import PhoneNumberBannedError


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

    def get_client(self) -> Client:
        return Client(
            session=DjangoSession(self.session),
            api_hash=self.app.api_hash,
            api_id=self.app.api_id,
            proxy=self.proxy.get_proxy_dict(),
        )

    def get_me(self):
        return _get_me(
            client=self.get_client(),
        )

    def get_dialogs(self):
        return _get_dialogs(
            client=self.get_client(),
        )

    def get_messages(self, chat_id, limit=1000):
        return _get_messages(
            client=self.get_client(),
            chat_id=chat_id,
            limit=limit,
        )

    def get_participants(self, chat_id, limit=1000):
        return _get_participants(
            client=self.get_client(),
            chat_id=chat_id,
        )

    def join_chat(self, chat_id):
        return _join_chat(
            client=self.get_client(),
            chat_id=chat_id,
        )

    def send_message(self, chat_id, text, reply_to_msg_id=None):
        return _send_message(
            client=self.get_client(),
            chat_id=chat_id,
            text=text,
            reply_to_msg_id=reply_to_msg_id,
        )

    def save_dialogs(self):
        for dialog in self.get_dialogs():
            if hasattr(dialog.entity, "title"):
                group, created = TelegramGroup.objects.get_or_create(
                    id=dialog.entity.id,
                    name=dialog.entity.title,
                    groupname=dialog.entity.username,
                )

    def save_messages(self, chat_id, limit=1000):
        group = TelegramGroup.objects.get(id=chat_id)
        for message in self.get_messages(chat_id=chat_id, limit=limit):
            if not message.text or message.text == "":
                continue
            user = None
            if message.from_id and hasattr(message.from_id, "user_id"):
                user, created = TelegramUser.objects.get_or_create(
                    id=message.from_id.user_id,
                    defaults={
                        "username": getattr(message.from_id, "username", None),
                        "first_name": getattr(message.from_id, "first_name", None),
                        "last_name": getattr(message.from_id, "last_name", None),
                        "lang_code": getattr(message.from_id, "lang_code", None),
                        "phone": getattr(message.from_id, "phone", None),
                        "sex": getattr(message.from_id, "sex", None),
                    },
                )
                reply_to_msg = (
                    group.messages.filter(
                        message_id=message.reply_to.reply_to_msg_id
                    ).first()
                    if message.reply_to and hasattr(message.reply_to, "reply_to_msg_id")
                    else None
                )
                group.messages.get_or_create(
                    message_id=message.id,
                    defaults={
                        "text": message.text,
                        "date": message.date,
                        "user": user,
                        "reply_to_msg": reply_to_msg,
                    },
                )
