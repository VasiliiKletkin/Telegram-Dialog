from core.celery import app
from .models import TelegramGroupSource


@app.task
def save_messages_from_groups():
    sources: list[TelegramGroupSource] = TelegramGroupSource.active.all()
    for source in sources:
        source.save_messages()
