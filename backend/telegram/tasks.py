from core.celery import app
from django_telethon.sessions import DjangoSession
from proxies.tasks import check_proxy
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from asgiref.sync import async_to_sync

from .models import TelegramUser


@app.task()
def check_user(id):
    telegram_user = TelegramUser.objects.get(id=id)
    check_proxy(telegram_user.proxy_server_id)

    try:
        if not telegram_user.proxy_server.is_active:
            raise Exception

        @async_to_sync
        async def checking():
            telegram_client = TelegramClient(
                session=DjangoSession(
                    client_session=telegram_user.client_session),
                api_id=telegram_user.app.api_id,
                api_hash=telegram_user.app.api_hash,
                proxy=telegram_user.proxy_server.get_proxy_dict(),
            )

            if not telegram_client.is_user_authorized():
                raise Exception

            async with telegram_client:
                await telegram_client.get_me()
                await telegram_client.get_dialogs()
        checking()

        telegram_user.is_active = True
    except Exception:
        telegram_user.is_active = False
    finally:
        telegram_user.save()


@app.task()
def send_message(telegram_user_id, chat_id, message):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)

    @async_to_sync
    async def send_mess():
        telegram_client = TelegramClient(
            session=DjangoSession(client_session=telegram_user.client_session),
            api_id=telegram_user.app.api_id,
            api_hash=telegram_user.app.api_hash,
            proxy=telegram_user.proxy_server.get_proxy_dict(),
        )

        async with telegram_client:
            await telegram_client.send_message(chat_id, message)
    send_mess()


@app.task()
async def join_to_chat(telegram_user_id, chat_id):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)

    @async_to_sync
    async def join():
        telegram_client = TelegramClient(
            session=DjangoSession(client_session=telegram_user.client_session),
            api_id=telegram_user.app.api_id,
            api_hash=telegram_user.app.api_hash,
            proxy=telegram_user.proxy_server.get_proxy_dict(),
        )
        async with telegram_client:
            chat = await telegram_client.get_entity(chat_id)
            await telegram_client(JoinChannelRequest(chat))
    join()
