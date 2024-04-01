import random
from django.db.models.signals import post_save
from django.dispatch import receiver

from telegram.models import TelegramUser
from .models import Scene


@receiver(post_save, sender=Scene)
def post_save_scene(sender, instance, created, **kwargs):
    if instance.roles_count < instance.dialog.roles_count:
        for _ in range(instance.dialog.roles_count - instance.roles_count):
            available_users_id = (
                TelegramUser.objects.filter(is_active=True)
                .exclude(
                    id__in=instance.roles.values_list("telegram_user_id", flat=True)
                )
                .values_list("id", flat=True)
            )
            if not available_users_id:
                available_users_count = TelegramUser.objects.filter(
                    is_active=True
                ).count()
                raise RuntimeError(
                    f"We have only {available_users_count} users, but in dialog {instance.dialog.roles_count} roles"
                )

            available_name_roles = (
                instance.dialog.messages.exclude(
                    role_name__in=instance.roles.values_list("name", flat=True)
                )
                .values_list("role_name", flat=True)
                .distinct()
            )

            instance.roles.create(
                telegram_user_id=random.choice(available_users_id),
                name=random.choice(available_name_roles),
            )
