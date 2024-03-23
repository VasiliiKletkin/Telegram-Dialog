from datetime import timedelta
import json

from core.celery import app
from django.db.models import Q
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from telegram.models import TelegramUser
from telegram.tasks import check_user, join_to_chat

from .models import Scene


@app.task()
def check_scene(id):
    scene = Scene.objects.get(id=id)

    roles = scene.roles.all()
    telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()

    try:
        if scene.roles_count != scene.dialog.roles_count:
            raise Exception(
                "Count of roles of Dialog are not equal count of roles of scene"
            )

        for user in telegram_users:
            check_user(user.id)
            if not user.is_ready:
                raise Exception(f"User {user} is not ready")

            if not user.client_session.entity_set.filter(
                Q(name=scene.telegram_group.name)
                | Q(username=scene.telegram_group.username)
            ).exists():
                join_to_chat(user.id, scene.telegram_group.username)

    except Exception as error:
        scene.error = str(error)
        scene.is_active = False
    else:
        scene.error = None
        scene.is_active = True
    finally:
        scene.save()


@app.task()
def start_scene(id):
    scene = Scene.objects.get(id=id)

    if not scene.is_ready:
        raise Exception("scene in not ready")

    for message in scene.dialog.messages.order_by("time"):
        role = scene.roles.get(name=message.role_name)

        target_time = timezone.now() + timedelta(
            seconds=message.time.second,
            minutes=message.time.minute,
            hours=message.time.hour,
        )
        target_time_str = target_time.strftime("%d-%b-%Y:%H:%M:%S")

        clocked_schedule = ClockedSchedule.objects.create(clocked_time=target_time)

        task = PeriodicTask.objects.create(
            clocked=clocked_schedule,
            name=f"Send message id:{message.id}, user_id:{role.telegram_user.id}, group:@{scene.telegram_group.username}, time:{target_time_str}, message:{message.text[:15]}",
            one_off=True,
            task="telegram.tasks.send_message",
            args=json.dumps(
                [
                    message.id,
                    scene.id,
                ]
            ),
        )
