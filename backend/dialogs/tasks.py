from core.celery import app
from django.db.models import Q
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from telegram.models import TelegramUser
from telegram.tasks import check_user, join_to_chat, send_message

from .models import Scene


@app.task()
def check_scene(id):
    scene = Scene.objects.get(id=id)

    roles = scene.roles.all()
    telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()

    for user in telegram_users:
        check_user(user.id)

    try:
        if roles.count() != scene.dialog.roles_count:
            raise Exception(
                "Count of roles of Dialog are not equal count of roles of scene"
            )

        users_with_problems = telegram_users.filter(is_active=False)
        if users_with_problems.exists():
            errors = ""
            for user in users_with_problems:
                errors += user.error + "\n"
            raise Exception(f"Some user(s) have problems:{errors}")

        for user in telegram_users:
            # FIXME change on more better option
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

    msg = None
    for message in scene.dialog.messages.all():
        role = scene.roles.get(role=message.role)

        # target_time = timezone.now() + timedelta(minutes=5)

        # clocked_schedule = ClockedSchedule.objects.create(clocked_time=target_time)

        # PeriodicTask.objects.create(
        #     clocked=clocked_schedule,
        #     name="my-task",
        #     description="Send message",
        #     one_off=True,
        #     task="telegram.tasks.send_message",
        #     args=[3, 7]
        # )
        msg_id = msg.id if msg else None
        msg = send_message(
            role.telegram_user.id,
            scene.telegram_group.username,
            message.text,
            reply_to_msg_id=msg_id,
        )
