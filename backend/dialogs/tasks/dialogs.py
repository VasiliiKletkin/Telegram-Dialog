import random
from datetime import datetime, timedelta
from typing import List
from django.utils.timezone import now
from core.celery import app
from dialogs.models import Dialog
from telegram_groups.models.sources import TelegramGroupSource
from telegram_messages.models import TelegramGroupMessage


@app.task()
def generate_dialog_from_source(source_id: int, date_from: datetime, date_to: datetime):
    source = TelegramGroupSource.objects.get(id=source_id)
    source_messages: List[TelegramGroupMessage] = source.messages.filter(
        date__range=(date_from, date_to)
    ).order_by("date")
    dialog = Dialog.objects.create(
        is_active=True,
        name=f"{source.name} {date_from.strftime('%Y.%m.%d %H:%M:%S')}-{date_to.strftime('%Y.%m.%d %H:%M:%S')}",
    )

    for message in source_messages:
        reply_to_msg = None
        if message.reply_to_msg:
            reply_to_msg = (
                dialog.messages.filter(
                    text=message.reply_to_msg.text,
                    role_name=str(message.reply_to_msg.user.id),
                )
                .order_by("-delay")
                .first()
            )
        dialog.messages.create(
            role_name=str(message.user.id),
            text=message.text,
            delay=message.date - date_from,
            reply_to_msg=reply_to_msg,
        )
    return dialog


@app.task()
def generate_scenes_every_day():
    date_to = now()
    date_from = date_to - timedelta(days=1)
    for source in TelegramGroupSource.active.all():
        dialog = generate_dialog_from_source(
            source_id=source.id,
            date_from=date_from,
            date_to=date_to,
        )
        for drain in source.drains.all():
            offset = timedelta(
                hours=random.randint(0, 2),
                minutes=random.randint(0, 30),
                seconds=random.randint(0, 60),
            )
            drain.scenes.create(
                dialog=dialog,
                is_active=True,
                start_date=date_to + offset,
            )
