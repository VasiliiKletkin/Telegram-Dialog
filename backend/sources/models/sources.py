from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from telegram.models import TelegramGroup
# from roles.models import ActorUser, ListenerUser


class TelegramGroupSource(TelegramGroup):

    # listeners = models.ManyToManyField(
    #     ListenerUser,
    #     related_name="listener_sources",
    #     blank=True,
    # )

    # actors = models.ManyToManyField(
    #     ActorUser,
    #     related_name="actor_sources",
    #     blank=True,
    #     through="TelegramGroupRole",
    # )

    errors = models.TextField(null=True, blank=True)

    @property
    def is_ready(self):
        return all(listener.is_member(self.id) for listener in self.listeners.all())

    def check_source(self):
        try:
            errors = ""
            for listener in self.listeners.all():
                if not listener.is_member(self.id):
                    errors += f"{listener} is not member of {self},"
            if errors:
                raise Exception(f"Listeners:{errors}")
        except Exception as e:
            self.errors = str(e)
        else:
            self.errors = None
        finally:
            self.save()

    def get_messages(self, limit=1000):
        pass

    def get_members(self):
        pass

    def create_roles_with_available_actors(self):
        roles = self.roles.all()
        available_actors = ActorUser.objects.exclude(actor_roles__in=roles)
        members = self.members.all()

        if members.count() < available_actors.count():
            raise ValidationError(
                f"Available actors{available_actors.count()} more than members{members.count()}"
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
