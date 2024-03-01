from asgiref.sync import async_to_sync
from django_telethon.sessions import DjangoSession
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from .models import TelegramUser


@async_to_sync
async def send_message(telegram_user_id, chat_id, message):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)

    telegram_client = TelegramClient(
        session=DjangoSession(client_session=telegram_user.session),
        api_id=telegram_user.app.api_id,
        api_hash=telegram_user.app.api_hash,
        proxy=telegram_user.proxy_server.get_proxy_dict(),
    )

    async with telegram_client:
        await telegram_client.send_message(chat_id, message)


@async_to_sync
async def join_to_chat(telegram_user_id, chat_id):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)

    telegram_client = TelegramClient(
        session=DjangoSession(client_session=telegram_user.session),
        api_id=telegram_user.app.api_id,
        api_hash=telegram_user.app.api_hash,
        proxy=telegram_user.proxy_server.get_proxy_dict(),
    )

    async with telegram_client:
        chat = telegram_client.get_entity(chat_id)
        await telegram_client(JoinChannelRequest(chat))
