from django.db import models
from .groups import TelegramGroup
from .users import TelegramUser


class TelegramGroupMessage(models.Model):
    group = models.ForeignKey(
        TelegramGroup, on_delete=models.CASCADE, related_name="messages"
    )
    message_id = models.BigIntegerField()
    text = models.TextField()
    date = models.DateTimeField()
    user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="messages"
    )
    reply_to_msg = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "message_id"],
                name="group_message_id_unique",
            )
        ]
        indexes = [
            models.Index(fields=["message_id"], name="message_id_idx"),
        ]

    def __str__(self):
        return f"mes_id:{self.message_id} - {self.group.get_groupname()} - {self.text[:20]}"
