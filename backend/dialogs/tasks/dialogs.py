import random
from datetime import timedelta
from typing import List
from django.utils.timezone import now
from core.celery import app
from telegram_groups.models.sources import TelegramGroupSource


@app.task()
def generate_scenes_every_day():
    date_to = now()
    date_from = date_to - timedelta(days=1)
    sources: List[TelegramGroupSource] = TelegramGroupSource.active.all()
    for source in sources:
        dialog = source.generate_dialog(
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
