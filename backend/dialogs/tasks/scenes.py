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

# @app.task()
# def generate_scenes_from_dialog(dialog_id):
#     dialog = Dialog.objects.get(id=dialog_id)
#     if not dialog.is_active:
#         return

#     if not dialog.telegram_group:
#         return

#     telegram_groups = TelegramGroup.objects.filter(
#         is_active=True, similar_groups__in=[dialog.telegram_group]
#     )
#     for telegram_group in telegram_groups:
#         start_date = dialog.date.replace(day=timezone.now().day) + timedelta(
#             days=random.randint(0, 7),
#             minutes=random.randint(0, 30),
#             seconds=random.randint(0, 60),
#         )

#         scene, created = Scene.objects.get_or_create(
#             telegram_group=telegram_group,
#             dialog=dialog,
#             defaults={"start_date": start_date},
#         )