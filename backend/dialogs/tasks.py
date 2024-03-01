from core.celery import app
from .models import Scene
from telegram.tasks import send_message


@app.task()
def start_dialogs(id):
    scene = Scene.objects.get(id=id)
    for message in scene.dialog.messages.all():
        role = scene.roles.get(role=message.role)
        send_message(scene.group.username, message.text, role.telegram_user.id)
        # role.telegram_user.send_message(
        #     scene.group.username, message.text)
