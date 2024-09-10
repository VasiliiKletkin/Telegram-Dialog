from datetime import time

from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from model_utils.models import TimeStampedModel


class Dialog(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            # models.Index(fields=["name"], name="name_idx"),
        ]

    def __str__(self):
        return f"{self.name[:50]}-{self.roles_count} roles"

    @property
    def roles_count(self):
        return self.messages.values("role_name").distinct().count()

    @property
    def messages_count(self):
        return self.messages.count()

    def get_roles_list(self):
        return self.messages.values_list("role_name").distinct()


class DialogMessage(TimeStampedModel):
    dialog = models.ForeignKey(
        Dialog,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role_name = models.CharField(max_length=255)
    text = models.TextField()
    start_time = models.TimeField(default=time(0))
    reply_to_msg = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        indexes = [
            # models.Index(fields=["role_name"], name="role_name_idx"),
            # models.Index(fields=["start_time"], name="start_time_idx"),
        ]

    def __str__(self):
        return f"{self.id}-{self.role_name}-{self.text[:10]}"

    def clean(self) -> None:
        if self.reply_to_msg and self.reply_to_msg.dialog != self.dialog:
            raise ValidationError("reply_to_msg link on different dialog")
        if self.reply_to_msg.id == self.id:
            raise ValidationError("reply_to_msg link to it self")
        return super().clean()
