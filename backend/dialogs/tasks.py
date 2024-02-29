from core.celery import app
from .models import Scene


@app.task()
def start_dialogs(id):
    scene = Scene.objects.get(id=id)
    for message in scene.dialog.messages.all():
        role = scene.roles.get(role=message.role)
        role.telegram_user.send_message(
            scene.group.username, message.text)
