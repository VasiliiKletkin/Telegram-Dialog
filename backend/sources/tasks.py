from datetime import timedelta

from core.celery import app
from dialogs.models import Dialog
from django.db.models import Count
from .utils import get_answer_from_message, get_dialog_messages_from_dict, 
from datetime import timedelta

from core.celery import app
from dialogs.models import Dialog
from django.db.models import Count
from .models import TelegramGroupSource as TelegramGroup




@app.task()
def save_messages_from_group(group_id):
    telegram_group = TelegramGroup.objects.get(id=group_id)
    ids = telegram_group.telegram_users.values_list("id", flat=True)
    telegram_user = TelegramUser.get_random(include_ids=ids)

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

        user = None
        if message.from_id and hasattr(message.from_id, "user_id"):
            user, created = TelegramUser.objects.get_or_create(
                id=message.from_id.user_id,
                defaults={
                    "username": message.from_id.username,
                    "first_name": message.from_id.first_name,
                    "last_name": message.from_id.last_name,
                },
            )
        TelegramGroupMessage.objects.get_or_create(
            message_id=message.id,
            telegram_group=telegram_group,
            defaults={
                "text": message.text,
                "date": message.date,
                "user": user,
                "reply_to_msg_id": (
                    message.reply_to.reply_to_msg_id
                    if message.reply_to and hasattr(message.reply_to, "reply_to_msg_id")
                    else None
                ),
            },
        )


@app.task()
def get_spammer_users(group_id):
    group = TelegramGroup.objects.get(id=group_id)
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
