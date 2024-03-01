from core.celery import app
from telegram.models import TelegramUser
from .models import Scene
from telegram.tasks import send_message
from telegram.tasks import check_user


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
    roles = scene.roles.all()
    telegram_users_is_not_active = TelegramUser.objects.filter(
        roles__in=roles, is_active=False).exists()

    if telegram_users_is_not_active:
        scene.is_active = False
