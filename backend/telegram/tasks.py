from datetime import timedelta
import random
import time

from asgiref.sync import async_to_sync
from core.celery import app
from django.conf import settings
from django.db.models import F
from django_telethon.models import UpdateState
from django_telethon.sessions import DjangoSession
from proxies.tasks import check_proxy
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from .models import TelegramGroup, TelegramGroupMessage, TelegramUser
from dialogs.models import Dialog, Message, Scene
from django.db.models import Count


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
            # await telegram_client.start(
            #     phone=telegram_user.phone, password=telegram_user.two_fa
            # )
            async with telegram_client:
                me = await telegram_client.get_me()
                await telegram_client.get_dialogs()
                telegram_user.first_name = me.first_name
                telegram_user.last_name = me.last_name
                telegram_user.username = me.username
                telegram_user.save(
                    update_fields=["first_name", "last_name", "username"]
                )

        checking()

    except Exception as error:
        telegram_user.error = str(error)
        telegram_user.is_active = False
    else:
        telegram_user.error = None
        telegram_user.is_active = True
    finally:
        telegram_user.save()


# @app.task()
# def send_message(telegram_user_id, chat_id, text, reply_to_msg_id=None, waiting=False):
#     telegram_user = TelegramUser.objects.get(id=telegram_user_id)

#     if waiting:
#         symbols_per_sec = (
#             random.randint(settings.MIN_SYMBOLS_PER_MIN, settings.MAX_SYMBOLS_PER_MIN)
#             / 60
#         )
#         wait_time = len(text) / symbols_per_sec
#         time.sleep(wait_time)

#     @async_to_sync
#     async def send_mess():
#         telegram_client = TelegramClient(
#             session=DjangoSession(client_session=telegram_user.client_session),
#             api_id=telegram_user.app.api_id,
#             api_hash=telegram_user.app.api_hash,
#             proxy=telegram_user.proxy_server.get_proxy_dict(),
#         )
#         UpdateState.objects.all().delete()
#         async with telegram_client:
#             chat = await telegram_client.get_entity(chat_id)
#             message = await telegram_client.send_message(
#                 chat, text, reply_to=reply_to_msg_id
#             )
#         TelegramGroupMessage.objects.create(
#             telegram_group=TelegramGroup.objects.get(username=chat.username),
#             message_id=message.id,
#             text=message.message,
#             date=message.date,
#             user_id=(
#                 message.from_id.user_id
#                 if message.from_id and hasattr(message.from_id, "user_id")
#                 else None
#             ),
#             reply_to_msg_id=(
#                 message.reply_to.reply_to_msg_id if message.reply_to else None
#             ),
#         )

#     send_mess()


@app.task()
def send_message(message_id, scene_id):
    scene = Scene.objects.get(id=scene_id)
    message = Message.objects.get(id=message_id)
    role = scene.roles.get(name=message.role_name)
    telegram_user = role.telegram_user

    reply_to_msg_id = None
    if answer_message := message.reply_to_msg:
        answer_role = scene.roles.get(name=answer_message.role_name)
        answer_telegram_user = answer_role.telegram_user
        try:
            reply_to_msg_id = (
                TelegramGroupMessage.objects.values_list("message_id", flat=True)
                .filter(
                    user_id=answer_telegram_user.id,
                    telegram_group=scene.telegram_group,
                    text=answer_message.text,
                )
                .order_by("date")
                .last()
            )
        except TelegramGroupMessage.DoesNotExist:
            pass

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
            chat = await telegram_client.get_entity(scene.telegram_group.username)
            sent_message = await telegram_client.send_message(
                chat,
                message.text,
                reply_to=reply_to_msg_id,
            )

        TelegramGroupMessage.objects.create(
            telegram_group=scene.telegram_group,
            message_id=sent_message.id,
            text=sent_message.message,
            date=sent_message.date,
            user_id=sent_message.from_id.user_id,
            reply_to_msg_id=(
                sent_message.reply_to.reply_to_msg_id if sent_message.reply_to else None
            ),
        )

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
                TelegramGroupMessage.objects.get_or_create(
                    message_id=message.id,
                    telegram_group=telegram_group,
                    defaults={
                        "text": message.text,
                        "date": message.date,
                        "user_id": (
                            message.from_id.user_id
                            if message.from_id and hasattr(message.from_id, "user_id")
                            else None
                        ),
                        "reply_to_msg_id": (
                            message.reply_to.reply_to_msg_id
                            if message.reply_to
                            and hasattr(message.reply_to, "reply_to_msg_id")
                            else None
                        ),
                    },
                )

    get_mess()


def get_answer_from_message(all_messages_from_group, ask_message):
    answer_messages = all_messages_from_group.filter(
        reply_to_msg_id=ask_message.message_id
    )
    dialogs_dict = {}
    for msg in answer_messages:
        dialogs_dict[msg] = get_answer_from_message(all_messages_from_group, msg)

        context_messages = all_messages_from_group.filter(
            message_id__in=range(msg.message_id + 1, msg.message_id + 3),
            user_id=msg.user_id,
            reply_to_msg_id__isnull=True,
        )
        for m in context_messages:
            dialogs_dict[m] = get_answer_from_message(all_messages_from_group, m)
    return dialogs_dict


def create_messages(dialog_id, messages_dict, reply_to_msg_id=None):
    msgs = []
    if isinstance(messages_dict, dict) and messages_dict == {}:
        return msgs
    for message, reply_messages in messages_dict.items():
        msg, created = Message.objects.get_or_create(
            dialog_id=dialog_id,
            text=message.text,
            defaults={
                "role_name": message.user_id if message.user_id else "Smbd",
                "start_time": message.date,
                "reply_to_msg_id": reply_to_msg_id,
            },
        )
        msgs.append(msg.id)
        msgs.extend(create_messages(dialog_id, reply_messages, reply_to_msg_id=msg.id))
    return msgs


@app.task()
def generate_dialogs_from_group(id):
    telegram_group = TelegramGroup.objects.get(id=id)
    messages_from_group = telegram_group.messages.all()

    answers_messages_ids = list(
        messages_from_group.values_list("reply_to_msg_id", flat=True)
        .annotate(count=Count("id"))
        .filter(count__gte=1)
    )

    messages_with_reply = messages_from_group.filter(
        message_id__in=answers_messages_ids, reply_to_msg_id__isnull=True
    )

    dialogs = {}
    for msg in messages_with_reply:

        context_messages = messages_from_group.filter(
            user_id=msg.user_id,
            message_id__in=range(msg.message_id - 2, msg.message_id + 2),
        )
        if context_messages.filter(reply_to_msg_id__isnull=False).exists():
            continue

        dialog = {}
        key = f"{telegram_group.name[:50]}:{msg.text[:100]}:{msg.user_id}"
        dialogs[key] = dialog

        for m in context_messages:
            dialog[m] = get_answer_from_message(messages_from_group, m)

        dialog, created = Dialog.objects.get_or_create(name=key[:255])
        # add auto tagging

        msg_ids = create_messages(dialog.id, dialogs[key])
        Message.objects.filter(id__in=msg_ids).update(
            time=F("start_time")
            - timedelta(seconds=msg.second, minutes=msg.minute, hours=msg.hour)
        )
