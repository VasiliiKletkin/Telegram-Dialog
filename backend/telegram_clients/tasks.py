from core.celery import app
# from proxies.tasks import check_proxy
from telethon.errors import PhoneNumberBannedError
from telegram.models import TelegramGroup
from .models import TelegramClient
from telegram.models import TelegramUser
from .utils import (
    get_dialogs,
    get_me,
    join_to_chat,
)


@app.task()
def update_user(user_id):
    user = TelegramUser.objects.get(id=user_id)
    client: TelegramClient = user.client

    me = get_me(
        client_session=client.session,
        api_id=client.app.api_id,
        api_hash=client.app.api_hash,
        proxy_dict=client.proxy.get_proxy_dict(),
    )

    user.first_name = me.first_name or user.first_name
    user.last_name = me.last_name or user.last_name
    user.username = me.username or user.username
    user.lang_code = me.lang_code or user.lang_code
    user.phone = me.phone or user.phone
    user.save()


# @app.task()
# def check_client(client_id):
#     try:
#         client = TelegramClient.objects.get(id=client_id)
#         proxy_server = client.proxy

#         if not proxy_server:
#             raise Exception("Proxy does not exist")

#         check_proxy(proxy_server.id)
#         proxy_server.refresh_from_db()

#         if not proxy_server.is_active:
#             raise Exception("Proxy is not active")
#         elif not proxy_server.is_ready:
#             raise Exception("Proxy is not ready")
#         elif proxy_server.errors:
#             raise Exception(f"Proxy error:{proxy_server.errors}")

#         update_user(client.user.id)
#     except PhoneNumberBannedError as error:
#         client.errors = str(error)
#         client.is_active = False

#     except Exception as error:
#         client.errors = str(error)
#     else:
#         client.errors = None
#     finally:
#         client.save()


@app.task()
def join_user_to_chat(user_id, chat_id):
    user = TelegramUser.objects.get(id=user_id)
    client: TelegramClient = user.client
    join_to_chat(
        client_session=client.session,
        api_id=client.app.api_id,
        api_hash=client.app.api_hash,
        proxy_dict=client.proxy.get_proxy_dict(),
        chat_id=chat_id,
    )


@app.task()
def save_dialogs_from_user(telegram_user_id):
    user = TelegramUser.objects.get(id=telegram_user_id)
    client: TelegramClient = user.client
    dialogs = get_dialogs(
        client_session=client.session,
        api_id=client.app.api_id,
        api_hash=client.app.api_hash,
        proxy_dict=client.proxy.get_proxy_dict(),
    )

    for dialog in dialogs:
        if hasattr(dialog.entity, "title"):
            group, created = TelegramGroup.objects.get_or_create(
                name=dialog.entity.title,
                groupname=dialog.entity.username,
            )
            user.groups.add(group)
