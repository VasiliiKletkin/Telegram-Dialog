import random
from django.db.models.signals import post_save
from django.dispatch import receiver

from telegram_users.models import ActorUser
from .models import Scene


@receiver(post_save, sender=Scene)
def post_save_scene(sender, instance: Scene, created, **kwargs):
    if instance.roles_count < instance.dialog.roles_count:

        for _ in range(instance.dialog.roles_count - instance.roles_count):

            available_actors = ActorUser.active.exclude(
                id__in=instance.actors.values_list("id", flat=True)
            )

            if not available_actors:
                actors_count = ActorUser.active.count()
                raise RuntimeError(
                    f"We have only {actors_count} actors, but in dialog {instance.dialog.roles_count} roles"
                )
            available_name_roles = instance.dialog.role_names(role_name__in=instance.role_names)
            instance.roles.create(
                actor=random.choice(available_actors),
                name=random.choice(available_name_roles),
            )
