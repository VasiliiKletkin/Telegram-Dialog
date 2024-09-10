from telegram_groups.models import TelegramGroupSource
from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel
from telegram_users.models import ActorUser, MemberUser


class TelegramGroupRole(TimeStampedModel):
    source = models.ForeignKey(
        TelegramGroupSource,
        on_delete=models.CASCADE,
        related_name="roles",
    )
    member = models.ForeignKey(
        MemberUser,
        on_delete=models.CASCADE,
        related_name="member_roles",
    )
    actor = models.ForeignKey(
        ActorUser,
        on_delete=models.CASCADE,
        related_name="actor_roles",
    )

    def clean(self) -> None:
        super().clean()
        if not self.member.is_member(self.source.id):
            raise ValidationError("Member must be member of the group")
        if self.member == self.actor:
            raise ValidationError("Member must not be equal actor")
        if self.source.listeners.filter(id=self.member.id).exists():
            raise ValidationError("Listener must not be member of the group")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "member"],
                name="group_member_unique",
            ),
            models.UniqueConstraint(
                fields=["source", "actor"],
                name="source_actor_unique",
            ),
        ]
