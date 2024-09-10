from django.db import models
from model_utils.models import TimeStampedModel
from telegram_users.models import TelegramUser


class TelegramGroup(TimeStampedModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    groupname = models.CharField(max_length=32, unique=True)
    members = models.ManyToManyField(
        TelegramUser,
        related_name="groups",
        blank=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["groupname"], name="groupname_idx"),
            models.Index(fields=["name"], name="name_idx"),
        ]

    def get_id(self):
        return -self.id

    def get_messages_count(self):
        return self.messages.count()

    def get_groupname(self):
        return f"@{self.groupname}"

    def __str__(self):
        return f"{self.name} - {self.get_groupname()}"