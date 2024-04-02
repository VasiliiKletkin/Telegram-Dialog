from datetime import time

from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager
from telegram.models import TelegramGroup, TelegramUser


class Dialog(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255, db_index=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"{self.name[:50]} {self.roles_count} roles"

    @property
    def roles_count(self):
        return self.messages.values("role_name").distinct().count()

    @property
    def messages_count(self):
        return self.messages.count()

    def get_roles_list(self):
        return self.messages.objects.values_list("role_name").distinct()


class Message(TimeStampedModel):
    dialog = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name="messages"
    )
    role_name = models.CharField(max_length=255, db_index=True)
    text = models.TextField(db_index=True)
    start_time = models.TimeField(default=time(0))
    reply_to_msg = models.ForeignKey(
        "Message", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id}, role:{self.role_name}, text:{self.text[:10]}"

    def clean(self) -> None:
        if self.reply_to_msg:
            if self.reply_to_msg.dialog != self.dialog:
                raise ValidationError("reply_to_msg link on different dialog")
        return super().clean()


class Scene(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    telegram_group = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="scenes")
    error = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("dialog", "telegram_group")

    def __str__(self):
        return f"{self.id}, dialog:{self.dialog.name}, group:@{self.telegram_group.username}"

    @property
    def is_ready(self):
        return (
            self.roles_count == self.dialog.roles_count
            and self.are_users_ready
            and self.are_users_members_of_group
            and self.is_active
            and not self.error
        )

    @property
    def roles_count(self):
        return self.roles.count()

    @property
    def are_users_ready(self):
        roles = self.roles.all()
        telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()
        return all(user.is_ready for user in telegram_users)

    @property
    def are_users_members_of_group(self):
        roles = self.roles.all()
        telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()
        return all(
            user.is_member_of_group(self.telegram_group.username)
            for user in telegram_users
        )


class Role(TimeStampedModel):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=255, db_index=True)
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="roles"
    )

    class Meta:
        unique_together = ("scene", "telegram_user", "name")

    def __str__(self):
        return f"name of role:{self.name}, username:{self.telegram_user}"

    # def clean(self):
    #     if (
    #         self.scene.roles.filter(telegram_user=self.telegram_user)
    #         .exclude(id=self.id)
    #         .exists()
    #     ):
    #         raise ValidationError("Role already exists")
