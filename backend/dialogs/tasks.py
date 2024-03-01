from core.celery import app
from telegram.models import TelegramUser
from .models import Scene
from telegram.tasks import send_message
from django.db.models import Q
from telegram.tasks import join_to_chat


@app.task()
def start_scene(id):
    scene = Scene.objects.get(id=id)
    for message in scene.dialog.messages.all():
        role = scene.roles.get(role=message.role)
        send_message(scene.group.username, message.text, role.telegram_user.id)
        # role.telegram_user.send_message(
        #     scene.group.username, message.text)


@app.task()
def check_scene(id):
    scene = Scene.objects.get(id=id)
    
    try:
        roles = scene.roles.all()

        telegram_users = TelegramUser.objects.filter(
            roles__in=roles)

        if telegram_users.filter(is_active=False).exists():
            raise Exception

        for user in telegram_users:
            if not user.client_session.entity_set.filter(Q(name=scene.group.name) | Q (username=scene.group.username)).exists():
                join_to_chat(user.id, scene.group.username)

    except Exception:
        scene.is_active = False

    finally:
        scene.save()