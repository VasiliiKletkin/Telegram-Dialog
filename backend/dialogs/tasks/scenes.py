import json
from datetime import timedelta
from django.utils import timezone

from core.celery import app
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from telegram_users.models import TelegramUser
from telegram_groups.models import TelegramGroup
import random
from ..models import Scene, Dialog, DialogMessage
from telegram_messages.models import TelegramGroupMessage
import json
from datetime import timedelta
from django.utils import timezone


from core.celery import app
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
import random
from ..models import Scene, Dialog, DialogMessage


@app.task()
def create_periodic_task_from_scene(scene_id):
    scene = Scene.objects.get(id=scene_id)

    start_time_str = scene.start_date.strftime("%d-%b-%Y:%H:%M:%S")
    clocked_schedule = ClockedSchedule.objects.create(clocked_time=scene.start_date)
    task_name = f"Start scene id:{scene.id}, time:{start_time_str}, group:{scene.telegram_group.username}, dialog:{scene.dialog.name},"
    PeriodicTask.objects.get_or_create(
        name=task_name[:200],
        defaults={
            "clocked": clocked_schedule,
            "enabled": scene.is_active,
            "one_off": True,
            "task": "dialogs.tasks.start_scene",
            "args": json.dumps([scene.id]),
        },
    )


@app.task()
def join_to_chat_users_from_scene(scene_id):
    scene = Scene.objects.get(id=scene_id)
    roles = scene.roles.all()
    telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()

    for telegram_user in telegram_users:
        if not telegram_user.is_member_of_group(scene.telegram_group.username):
            join_user_to_chat(
                telegram_user.id,
                scene.telegram_group.username,
            )
            save_dialogs_from_user(telegram_user.id)


@app.task()
def send_message_from_scene(message_id, scene_id):
    scene = Scene.objects.get(id=scene_id)
    message = DialogMessage.objects.get(id=message_id)
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

    # sent_message = send_message(
    #     client_session=telegram_user.client_session,
    #     api_id=telegram_user.app.api_id,
    #     api_hash=telegram_user.app.api_hash,
    #     proxy_dict=telegram_user.proxy_server.get_proxy_dict(),
    #     username=scene.telegram_group.username,
    #     text=message.text,
    #     reply_to_msg_id=reply_to_msg_id,
    # )

    # TelegramGroupMessage.objects.create(
    #     telegram_group=scene.telegram_group,
    #     message_id=sent_message.id,
    #     text=sent_message.message,
    #     date=sent_message.date,
    #     user_id=sent_message.from_id.user_id,
    #     reply_to_msg_id=(
    #         sent_message.reply_to.reply_to_msg_id if sent_message.reply_to else None
    #     ),
    # )


@app.task()
def generate_scenes_from_dialog(dialog_id):
    dialog = Dialog.objects.get(id=dialog_id)
    if not dialog.is_active:
        return

    if not dialog.telegram_group:
        return

    telegram_groups = TelegramGroup.objects.filter(
        is_active=True, similar_groups__in=[dialog.telegram_group]
    )
    for telegram_group in telegram_groups:
        start_date = dialog.date.replace(day=timezone.now().day) + timedelta(
            days=random.randint(0, 7),
            minutes=random.randint(0, 30),
            seconds=random.randint(0, 60),
        )

        scene, created = Scene.objects.get_or_create(
            telegram_group=telegram_group,
            dialog=dialog,
            defaults={"start_date": start_date},
        )
