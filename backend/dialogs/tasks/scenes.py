from core.celery import app
from ..models import Scene

@app.task()
def send_message_from_scene(scene_id, message_id):
    scene = Scene.objects.get(id=scene_id)
    scene.send_message(message_id)


@app.task()
def start_scene(scene_id):
    scene = Scene.objects.get(id=scene_id)
    scene.start()

