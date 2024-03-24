import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from .models import Scene


# @receiver(post_save, sender=Scene)
# def scene_save(sender, instance, **kwargs):
#     PeriodicTask.objects.create(
#         name=f"Start scene id:{instance.id}, dialog:{instance.dialog.name}, group:{instance.telegram_group.username}, time:{instance.clocked_schedule.clocked_time}",
#         defaults={
#             "clocked": instance.clocked_schedule,
#             "one_off": True,
#             "task": "dialogs.tasks.start_scene",
#             "args": json.dumps([instance.id]),
#         },
#     )
