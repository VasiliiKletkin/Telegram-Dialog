from datetime import timedelta

from core.celery import app
from dialogs.models import Dialog, Message, Scene
from django.db.models import Count
from proxies.tasks import check_proxy
from taggit.models import Tag
from telethon.errors import PhoneNumberBannedError

from .models import TelegramGroup, TelegramGroupMessage, TelegramUser
from .utils import (
    get_messages,
    get_tags_from_str,
    get_answer_from_message,
    get_dialog_messages_from_dict,
)


@app.task()
def generate_dialogs_from_group(group_id):
    save_messages_from_group(group_id)

    group = TelegramGroup.objects.get(id=group_id)
    messages = group.messages.all()

    if spammer_user_ids := get_spammer_users(group_id):  # фильтруем от спамеров
        messages = messages.exclude(user_id__in=spammer_user_ids)

    answers_messages_ids = list(  # получаем все id ответов
        messages.values_list("reply_to_msg_id", flat=True)
        .annotate(count=Count("id"))
        .filter(count__gte=1)
    )

    messages_with_reply = messages.filter(  # получаем сообщения с ответами но при это чтобы они сами не были ответами
        message_id__in=answers_messages_ids, reply_to_msg_id__isnull=True
    )

    for msg in messages_with_reply:
        context_messages = messages.filter(
            user_id=msg.user_id,
            message_id__in=range(msg.message_id - 2, msg.message_id + 3),
        )

        if msg.reply_to_msg_id:  # если сообщение является ответом на другое сообщение
            continue
        elif context_messages.filter(
            reply_to_msg_id__isnull=False
        ).exists():  # если контекст является ответом на другое сообщение
            continue

        dialog, created = Dialog.objects.get_or_create(
            name=msg.text[:255],
            defaults={"telegram_group": group, "date": msg.date},
        )

        if created:  # если диалог был создан только для тегов
            dialog.tags.add(*group.tags.all())
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

        dialog_dict = {
            m: get_answer_from_message(messages, m) for m in context_messages
        }
        dialog_messages_ids = get_dialog_messages_from_dict(dialog, delta, dialog_dict)
