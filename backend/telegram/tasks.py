import random
import time

from asgiref.sync import async_to_sync
from core.celery import app
from django.conf import settings
from django_telethon.models import UpdateState
from django_telethon.sessions import DjangoSession
from proxies.tasks import check_proxy
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import PeerUser
from .models import TelegramGroup, TelegramGroupMessage, TelegramUser


@app.task()
def check_user(id):
    try:
        telegram_user = TelegramUser.objects.get(id=id)

        if not telegram_user.proxy_server:
            raise Exception("Proxy does not exist")

        check_proxy(telegram_user.proxy_server_id)
        telegram_user.proxy_server.refresh_from_db()

        if not telegram_user.proxy_server.is_ready:
            raise Exception(f"Proxy is not ready:{telegram_user.proxy_server.error}")

        @async_to_sync
        async def checking():
            telegram_client = TelegramClient(
                session=DjangoSession(client_session=telegram_user.client_session),
                api_id=telegram_user.app.api_id,
                api_hash=telegram_user.app.api_hash,
                proxy=telegram_user.proxy_server.get_proxy_dict(),
            )
            UpdateState.objects.all().delete()
            await telegram_client.start(
                phone=telegram_user.phone, password=telegram_user.two_fa
            )

            async with telegram_client:
                await telegram_client.get_me()
                await telegram_client.get_dialogs()

        checking()

    except Exception as error:
        telegram_user.error = str(error)
        telegram_user.is_active = False
    else:
        telegram_user.error = None
        telegram_user.is_active = True
    finally:
        telegram_user.save()


@app.task()
def send_message(telegram_user_id, chat_id, message, reply_to_msg_id=None):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)

    symbols_per_sec = (
        random.randint(settings.MIN_SYMBOLS_PER_MIN, settings.MAX_SYMBOLS_PER_MIN) / 60
    )
    wait_time = len(message) / symbols_per_sec
    time.sleep(wait_time)

    @async_to_sync
    async def send_mess():
        telegram_client = TelegramClient(
            session=DjangoSession(client_session=telegram_user.client_session),
            api_id=telegram_user.app.api_id,
            api_hash=telegram_user.app.api_hash,
            proxy=telegram_user.proxy_server.get_proxy_dict(),
        )
        UpdateState.objects.all().delete()
        async with telegram_client:
            chat = await telegram_client.get_entity(chat_id)
            msg = await telegram_client.send_message(
                chat, message, reply_to=reply_to_msg_id
            )
        return msg

    return send_mess()


@app.task()
def join_to_chat(telegram_user_id, chat_id):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)

    @async_to_sync
    async def join():
        telegram_client = TelegramClient(
            session=DjangoSession(client_session=telegram_user.client_session),
            api_id=telegram_user.app.api_id,
            api_hash=telegram_user.app.api_hash,
            proxy=telegram_user.proxy_server.get_proxy_dict(),
        )
        UpdateState.objects.all().delete()
        async with telegram_client:
            chat = await telegram_client.get_entity(chat_id)
            await telegram_client(JoinChannelRequest(chat))

    join()


@app.task()
def get_messages_from_group(id):
    telegram_group = TelegramGroup.objects.get(id=id)
    telegram_user = TelegramUser.objects.filter(is_active=True).first()

    @async_to_sync
    async def get_mess():
        telegram_client = TelegramClient(
            session=DjangoSession(client_session=telegram_user.client_session),
            api_id=telegram_user.app.api_id,
            api_hash=telegram_user.app.api_hash,
            proxy=telegram_user.proxy_server.get_proxy_dict(),
        )
        UpdateState.objects.all().delete()
        async with telegram_client:
            group = await telegram_client.get_entity(telegram_group.username)
            async for message in telegram_client.iter_messages(group, 1000):
                if isinstance(message.from_id, PeerUser):
                    TelegramGroupMessage.objects.get_or_create(
                        message_id=message.id,
                        group=telegram_group,
                        defaults={
                            "text": message.text,
                            "date": message.date,
                            "user_id": message.from_id.user_id,
                            "reply_to_msg_id": (
                                message.reply_to.reply_to_msg_id
                                if message.reply_to
                                else None
                            ),
                        },
                    )

    get_mess()
