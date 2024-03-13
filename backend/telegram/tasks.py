from asgiref.sync import async_to_sync
from core.celery import app
from django_telethon.sessions import DjangoSession
from proxies.tasks import check_proxy
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from .models import TelegramGroup, TelegramUser, TelegramGroupMessage


@app.task()
def check_user(id):
    try:
        telegram_user = TelegramUser.objects.get(id=id)

        if not telegram_user.proxy_server:
            raise Exception("Proxy does not exist")

        check_proxy(telegram_user.proxy_server_id)

        if telegram_user.is_ready:
            raise Exception("Proxy does not ready")

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
                raise Exception("User is not authorized")

            async with telegram_client:
                await telegram_client.get_me()

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
            chat = await telegram_client.get_entity(chat_id)
            await telegram_client.send_message(chat, message)
    send_mess()


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
            session=DjangoSession(
                client_session=telegram_user.client_session),
            api_id=telegram_user.app.api_id,
            api_hash=telegram_user.app.api_hash,
            proxy=telegram_user.proxy_server.get_proxy_dict(),
        )
        async with telegram_client:
            group = await telegram_client.get_entity(telegram_group.username)
            for message in await telegram_client.iter_messages(group, 1000):
                TelegramGroupMessage.objects.create(message_id=message.id, user_id=message.from_id.user_id, group=telegram_group,
                                                    message=message.text, reply_to_msg_id=message.reply_to.reply_to_msg_id, date=message.date)
    get_mess()
