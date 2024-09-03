# trunk-ignore-all(isort)
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from telegram.models import TelegramGroup, TelegramUser
from model_utils.models import TimeStampedModel


class TelegramGroupSource(TelegramGroup):

    def download_messages(self, limit=1000):
        pass

    def create_roles_with_available_actors(self):
        roles = self.roles.all()
        available_actors = TelegramUser.objects.filter(client__isnull=False).exclude(
            actor_roles__in=roles
        )
        members = self.members.all()

        if members.count() > available_actors.count():
            raise ValidationError(
                f"Members count{members.count()} more than available actors count {available_actors.count()}"
            )
        for index, member in enumerate(members):
            roles.create(member=member, actor=available_actors[index])

    def update_roles(self):
        self.create_roles_with_available_actors()

        roles = self.roles.all()

        end_date = now()
        start_date = end_date - timedelta(days=7)
        members = (
            self.members.annotate(
                messages_count=models.Count(
                    "messages",
                    filter=models.Q(messages__date__range=(start_date, end_date)),
                )
            )
            .order_by("messages_count")
            .filter(messages_count__gt=0)
        )

        members_without_roles = members.filter(member_roles__isnull=True)
        unusable_roles = roles.exclude(member__in=members).order_by("-modified")

        if members_without_roles.count() > unusable_roles.count():
            raise ValidationError(
                f"Active members{members_without_roles.count()} more than available roles{unusable_roles.count()}"
            )
        for index, member in enumerate(members_without_roles):
            unusable_roles[index].update(member=member)

    class Meta:
        proxy = True


class TelegramGroupRole(TimeStampedModel):
    group = models.ForeignKey(
        TelegramGroupSource,
        on_delete=models.CASCADE,
        related_name="roles",
    )
    member = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="member_roles",
    )
    actor = models.ForeignKey(
        TelegramUser,
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
                fields=[
                    "group",
                    "member",
                    "actor",
                ],
                name="group_member_actor_unique",
            )
        ]
