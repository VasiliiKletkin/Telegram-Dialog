from datetime import timedelta

from core.celery import app
from dialogs.models import Dialog, Message, Scene
from django.conf import settings
from django.db.models import Count, F
from django_telethon.models import Entity
from proxies.tasks import check_proxy

from .models import TelegramGroup, TelegramGroupMessage, TelegramUser
from .utils import (get_dialogs, get_me, get_messages, join_to_chat,
                    send_message)


@app.task()
def save_dialogs_from_user(telegram_user_id):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)
    dialogs = get_dialogs(
        client_session=telegram_user.client_session,
        api_id=telegram_user.app.api_id,
        api_hash=telegram_user.app.api_hash,
        proxy_dict=telegram_user.proxy_server.get_proxy_dict(),
    )
    entities = []
    for dialog in dialogs:
        entities.append(
            Entity(
                entity_id=dialog.id,
                client_session=telegram_user.client_session,
                hash_value=dialog.entity.access_hash,
                username=dialog.entity.username,
                phone=(
                    dialog.entity.phone if hasattr(dialog.entity, "phone") else None
                ),
                name=(
                    dialog.entity.title
                    if hasattr(dialog.entity, "title")
                    else f"{dialog.entity.first_name} {dialog.entity.last_name}"
                ),
            )
        )
    telegram_user.client_session.entity_set.bulk_create(
        entities,
        ignore_conflicts=True,
    )


@app.task()
def check_user(user_id):
    try:
        telegram_user = TelegramUser.objects.get(id=user_id)
        proxy_server = telegram_user.proxy_server

        if not proxy_server:
            raise Exception("Proxy does not exist")

        check_proxy(proxy_server.id)
        proxy_server.refresh_from_db()

        if not proxy_server.is_active:
            raise Exception("Proxy is not active")
        elif not proxy_server.is_ready:
            raise Exception("Proxy is not ready")
        elif proxy_server.error:
            raise Exception(f"Proxy error:{proxy_server.error}")

        me = get_me(
            client_session=telegram_user.client_session,
            api_id=telegram_user.app.api_id,
            api_hash=telegram_user.app.api_hash,
            proxy_dict=telegram_user.proxy_server.get_proxy_dict(),
        )

        telegram_user.first_name = me.first_name
        telegram_user.last_name = me.last_name
        telegram_user.username = me.username

    except Exception as error:
        telegram_user.error = str(error)
    else:
        telegram_user.error = None
    finally:
        telegram_user.save()

    # save_all_dialogs_from_user.delay(user_id)


#     if waiting:
#         symbols_per_sec = (
#             random.randint(settings.MIN_SYMBOLS_PER_MIN, settings.MAX_SYMBOLS_PER_MIN)
#             / 60
#         )
#         wait_time = len(text) / symbols_per_sec
#         time.sleep(wait_time)


@app.task()
def send_message_from_scene(message_id, scene_id):
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

    sent_message = send_message(
        client_session=telegram_user.client_session,
        api_id=telegram_user.app.api_id,
        api_hash=telegram_user.app.api_hash,
        proxy_dict=telegram_user.proxy_server.get_proxy_dict(),
        username=scene.telegram_group.username,
        text=message.text,
        reply_to_msg_id=reply_to_msg_id,
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


@app.task()
def join_user_to_chat(telegram_user_id, chat_id):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)

    join_to_chat(
        client_session=telegram_user.client_session,
        api_id=telegram_user.app.api_id,
        api_hash=telegram_user.app.api_hash,
        proxy_dict=telegram_user.proxy_server.get_proxy_dict(),
        chat_id=chat_id,
    )

    save_dialogs_from_user.delay(telegram_user_id)


@app.task()
def get_messages_from_group(group_id):
    telegram_group = TelegramGroup.objects.get(id=group_id)
    telegram_user = TelegramUser.objects.filter(is_active=True).first()

    messages = get_messages(
        client_session=telegram_user.client_session,
        api_id=telegram_user.app.api_id,
        api_hash=telegram_user.app.api_hash,
        proxy_dict=telegram_user.proxy_server.get_proxy_dict(),
        username=telegram_group.username,
    )
    for message in messages:
        # FIXME change on bulk update
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
                    if message.reply_to and hasattr(message.reply_to, "reply_to_msg_id")
                    else None
                ),
            },
        )


def get_answer_from_message(all_messages_from_group, ask_message):
    answer_messages = all_messages_from_group.filter(
        reply_to_msg_id=ask_message.message_id
    )
    dialogs_dict = {}
    for msg in answer_messages:
        # ищем сообщения которые являются ответами на текущее сообщение
        dialogs_dict[msg] = get_answer_from_message(all_messages_from_group, msg)

        context_messages = all_messages_from_group.filter(
            message_id__in=range(msg.message_id + 1, msg.message_id + 3),
            user_id=msg.user_id,
            reply_to_msg_id__isnull=True,  # ищем сообщения которые не являются ответами в контексте
        )
        for m in context_messages:
            # проверям есть ли ответы на сообщения из контекста
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
def generate_dialogs_from_group(group_id):
    telegram_group = TelegramGroup.objects.get(id=group_id)
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
        if context_messages.filter(
            reply_to_msg_id__isnull=False
        ).exists():  # если текущий контекст является ответом на другое сообщение
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
            start_time=F("start_time")
            - timedelta(
                seconds=msg.date.second,
                minutes=msg.date.minute,
                hours=msg.date.hour,
            )
        )
