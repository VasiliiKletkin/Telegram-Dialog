from datetime import timedelta

from core.celery import app
from dialogs.models import Dialog
from django.db.models import Count
from .utils import get_answer_from_message, get_dialog_messages_from_dict
from datetime import timedelta
from core.celery import app
from dialogs.models import Dialog
from django.db.models import Count

from .models.sources import TelegramGroupSource
from telegram.models import TelegramGroupMessage, TelegramUser
from telegram_clients.utils import get_messages
from telegram_clients.models import TelegramClient


@app.task()
def save_messages_from_group(group_id):
    group = TelegramGroupSource.objects.get(id=group_id)
    client_ids = group.members.filter(
        client__isnull=False,
        client__is_active=True,
    ).values_list("client__id", flat=True)

    client = TelegramClient.get_random(include_ids=client_ids)

    messages = get_messages(
        client_session=client.session,
        api_id=client.app.api_id,
        api_hash=client.app.api_hash,
        proxy_dict=client.proxy.get_proxy_dict(),
        username=group.groupname,
    )
    for message in messages:
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
                group.messages.filter(message_id=message.reply_to.reply_to_msg_id).first()
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


@app.task()
def get_spammer_users(group_id):
    group = TelegramGroupSource.objects.get(id=group_id)
    messages = group.messages.all()

    user_ids_from_group = (
        messages.filter(user_id__isnull=False)
        .values_list("user_id", flat=True)
        .annotate(count=Count("id"))
        .filter(count__gte=10)
        .order_by("-count")[:10]
    )

    return [
        user_id
        for user_id in user_ids_from_group
        if (
            messages.filter(user_id=user_id)
            .values_list("text", flat=True)
            .annotate(count=Count("id"))
            .filter(count__gte=10)
            .exists()
        )
    ]
