import json
from datetime import timedelta
from django.utils import timezone

from core.celery import app
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from telegram.models import TelegramUser
from telegram.tasks import check_user, join_user_to_chat, save_dialogs_from_user
import random
from .models import Scene, TelegramGroupDialog


@app.task()
def check_scene(scene_id):
    scene = Scene.objects.get(id=scene_id)

    roles = scene.roles.all()
    telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()

    try:
        if scene.roles_count != scene.dialog.roles_count:
            raise Exception(
                "Count of roles of Dialog are not equal count of roles of scene"
            )
        join_to_chat_users_from_scene(scene.id)

        for user in telegram_users:
            check_user(user.id)
            user.refresh_from_db()

            if not user.is_active:
                raise Exception(f"User {user} is not active")
            elif not user.is_ready:
                raise Exception(f"User {user} is not ready")
            elif user.error:
                raise Exception(f"User {user} error: {user.error}")
            elif not user.is_member_of_group(scene.telegram_group.username):
                raise Exception(f"User {user} is not member of group")

    except Exception as error:
        scene.error = str(error)
    else:
        scene.error = None
    finally:
        scene.save()


@app.task()
def start_scene(scene_id):
    scene = Scene.objects.get(id=scene_id)

    check_scene(scene.id)
    scene.refresh_from_db()

    if not scene.is_ready:
        raise Exception("scene in not ready")

    for message in scene.dialog.messages.order_by("start_time"):
        role = scene.roles.get(name=message.role_name)

        target_time = timezone.now() + timedelta(
            seconds=message.start_time.second,
            minutes=message.start_time.minute,
            hours=message.start_time.hour,
        )
        target_time_str = target_time.strftime("%d-%b-%Y:%H:%M:%S")
        clocked_schedule = ClockedSchedule.objects.create(clocked_time=target_time)
        PeriodicTask.objects.create(
            clocked=clocked_schedule,
            name=f"Send message id:{message.id}, start_time:{target_time_str}, user_id:{role.telegram_user.id}, group:@{scene.telegram_group.username},  message:{message.text[:15]}",
            one_off=True,
            task="telegram.tasks.send_message_from_scene",
            args=json.dumps(
                [
                    message.id,
                    scene.id,
                ]
            ),
        )


@app.task()
def create_periodic_task_from_scene(scene_id):
    scene = Scene.objects.get(id=scene_id)

    if not scene.is_ready:
        raise Exception("scene in not ready")

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
def generate_scenes_from_dialog(telegram_dialog_id):
    telegram_dialog = TelegramGroupDialog.objects.get(id=telegram_dialog_id)
    if not telegram_dialog.dialog.is_active:
        return

    for telegram_group in telegram_dialog.telegram_group.similar_groups.filter(
        is_active=True
    ):
        start_date = telegram_dialog.date
        start_date = start_date.replace(day=timezone.now().day)
        start_date += timedelta(
            days=random.randint(0, 7),
            minutes=random.randint(0, 30),
            seconds=random.randint(0, 60),
        )

        scene, created = Scene.objects.get_or_create(
            telegram_group=telegram_group,
            dialog=telegram_dialog.dialog,
            defaults={"start_date": start_date},
        )
