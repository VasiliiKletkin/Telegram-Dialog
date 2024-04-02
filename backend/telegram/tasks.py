from datetime import timedelta

from telethon.errors import PhoneNumberBannedError
from core.celery import app
from dialogs.models import Dialog, Message, Scene
from django.db.models import Count, F
from proxies.tasks import check_proxy
from taggit.models import Tag

from .models import (
    TelegramGroup,
    TelegramGroupDialog,
    TelegramGroupMessage,
    TelegramUser,
)
from .utils import (
    get_dialogs,
    get_me,
    get_messages,
    get_tags_from_str,
    join_to_chat,
    send_message,
)


@app.task()
def save_dialogs_from_user(telegram_user_id):
    telegram_user = TelegramUser.objects.get(id=telegram_user_id)
    dialogs = get_dialogs(
        client_session=telegram_user.client_session,
        api_id=telegram_user.app.api_id,
        api_hash=telegram_user.app.api_hash,
        proxy_dict=telegram_user.proxy_server.get_proxy_dict(),
    )

    for dialog in dialogs:
        if hasattr(dialog.entity, "title"):
            telegram_group, created = TelegramGroup.objects.get_or_create(
                name=dialog.entity.title,
                username=dialog.entity.username,
            )
            telegram_user.telegram_groups.add(telegram_group)


@app.task()
def check_user(telegram_user_id):
    try:
        telegram_user = TelegramUser.objects.get(id=telegram_user_id)
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

    except PhoneNumberBannedError as error:
        telegram_user.error = str(error)
        telegram_user.is_active = False

    except Exception as error:
        telegram_user.error = str(error)
    else:
        telegram_user.error = None
    finally:
        telegram_user.save()


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
                    text=answer_message.text.replace("\r\n", " \n"),
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


@app.task()
def save_messages_from_group(group_id):
    telegram_group = TelegramGroup.objects.get(id=group_id)
    telegram_user = TelegramUser.get_random()

    messages = get_messages(
        client_session=telegram_user.client_session,
        api_id=telegram_user.app.api_id,
        api_hash=telegram_user.app.api_hash,
        proxy_dict=telegram_user.proxy_server.get_proxy_dict(),
        username=telegram_group.username,
    )
    for message in messages:
        # FIXME change on bulk update
        if not message.text or message.text == "":
            continue

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


def get_dialog_messages_from_dict(dialog, delta, messages_dict, reply_to_msg=None):
    dialog_messages = []
    if isinstance(messages_dict, dict) and messages_dict == {}:
        return dialog_messages
    for message, reply_messages_dict in messages_dict.items():
        msg, created = Message.objects.get_or_create(
            dialog=dialog,
            text=message.text,
            defaults={
                "role_name": message.user_id if message.user_id else "Smbd",
                "start_time": message.date - delta,
                "reply_to_msg": reply_to_msg,
            },
        )
        dialog_messages.append(msg.id)
        dialog_messages.extend(
            get_dialog_messages_from_dict(
                dialog,
                delta,
                reply_messages_dict,
                reply_to_msg=msg,
            )
        )
    return dialog_messages


@app.task()
def get_spammer_users(group_id):
    telegram_group = TelegramGroup.objects.get(id=group_id)
    group_messages = telegram_group.messages.all()

    user_ids_spammer = []

    user_ids_from_group = (
        group_messages.filter(user_id__isnull=False)
        .values_list("user_id", flat=True)
        .annotate(count=Count("id"))
        .filter(count__gte=10)
        .order_by("-count")[:10]
    )

    for user_id in user_ids_from_group:
        if (
            group_messages.filter(user_id=user_id)
            .values_list("text", flat=True)
            .annotate(count=Count("id"))
            .filter(count__gte=10)
            .exists()
        ):
            user_ids_spammer.append(user_id)

    return user_ids_spammer


@app.task()
def generate_dialogs_from_group(group_id):
    # save_messages_from_group(group_id)

    telegram_group = TelegramGroup.objects.get(id=group_id)
    group_messages = telegram_group.messages.all()

    if spammer_user_ids := get_spammer_users(group_id):  # фильтруем от спамеров
        group_messages = group_messages.exclude(user_id__in=spammer_user_ids)

    answers_messages_ids = list(  # получаем все id ответов
        group_messages.values_list("reply_to_msg_id", flat=True)
        .annotate(count=Count("id"))
        .filter(count__gte=1)
    )

    group_messages_with_reply = group_messages.filter(  # получаем сообщения с ответами но при это чтобы они сами не были ответами
        message_id__in=answers_messages_ids, reply_to_msg_id__isnull=True
    )

    for msg in group_messages_with_reply:
        context_messages = group_messages.filter(
            user_id=msg.user_id,
            message_id__in=range(msg.message_id - 2, msg.message_id + 3),
        )

        if msg.reply_to_msg_id:  # если сообщение является ответом на другое сообщение
            continue
        elif context_messages.filter(
            reply_to_msg_id__isnull=False
        ).exists():  # если контекст является ответом на другое сообщение
            continue

        dialog, created = Dialog.objects.get_or_create(name=msg.text[:255])
        TelegramGroupDialog.objects.get_or_create(
            group=telegram_group, dialog=dialog, date=msg.date
        )

        if created:
            dialog.tags.add(*telegram_group.tags.all())
            tags = []
            for tag_name in get_tags_from_str(msg.text):
                tag, created = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={
                        "slug": tag_name,
                    },
                )
                tags.append(tag)
            dialog.tags.add(*tags)

        delta = timedelta(
            seconds=msg.date.second,
            minutes=msg.date.minute,
            hours=msg.date.hour,
        )

        dialog_dict = {}
        for m in context_messages:
            dialog_dict[m] = get_answer_from_message(group_messages, m)

        dialog_messages_ids = get_dialog_messages_from_dict(dialog, delta, dialog_dict)
