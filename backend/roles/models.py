from groups.models import TelegramGroupSource
from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel
from users.models import ActorUser, MemberUser


class TelegramGroupRole(TimeStampedModel):
    group = models.ForeignKey(
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
        if not self.member.is_member(self.group.id):
            raise ValidationError("Member must be member of the group")
        if self.member == self.actor:
            raise ValidationError("Member must not be equal actor")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "member"],
                name="group_member_unique",
            ),
            models.UniqueConstraint(
                fields=["group", "actor"],
                name="group_actor_unique",
            ),
        ]
