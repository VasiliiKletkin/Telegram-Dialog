from django.db import models
from django.db.models import Q
from model_utils.models import TimeStampedModel
from telegram.models import TelegramGroup, TelegramUser
from taggit.managers import TaggableManager


class Dialog(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    tags = TaggableManager()

    def __str__(self):
        return f"{self.name} {self.roles_count} roles"

    @property
    def roles_count(self):
        return self.messages.values("role").distinct().count()


class Message(TimeStampedModel):
    dialog = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name="messages"
    )
    role_name = models.CharField(max_length=255)
    text = models.TextField()
    time = models.TimeField()
    reply_to_msg = models.ForeignKey(
        "Message", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id}:{self.role}: {self.text[:10]}"


class Scene(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="scenes")
    telegram_group = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.dialog.name} {self.telegram_group.username}"

    @property
    def is_ready(self):
        roles = self.roles.all()
        telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()
        are_users_active = all(user.is_ready for user in telegram_users)
        are_users_members_of_group = all(
            user.client_session.entity_set.filter(
                Q(name=self.telegram_group.name)
                | Q(username=self.telegram_group.username)
            ).exists()
            for user in telegram_users
        )
        return (
            self.roles_count == self.dialog.roles_count
            and are_users_active
            and are_users_members_of_group
            and self.is_active
        )

    @property
    def roles_count(self):
        return self.roles.count()

    # def clean(self) -> None:
    #     self.dialog.

    #     return super().clean()


class Role(TimeStampedModel):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=255)
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="roles"
    )

    def __str__(self):
        return f"{self.telegram_user.username} {self.name}"

    class Meta:
        unique_together = ("scene", "telegram_user", "name")
