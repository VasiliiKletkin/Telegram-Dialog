from .base import BaseGroupModel
from django.db import models
from .sources import TelegramGroupSource
from django.utils.timezone import now

from telegram_users.models import ActorUser


class TelegramGroupDrain(BaseGroupModel):
    sources = models.ManyToManyField(
        TelegramGroupSource, related_name="drains", blank=True
    )

    @property
    def is_ready(self):
        return (
            self.is_active
            and not self.errors
            and bool(self.last_check)
            and all(
                actor.is_ready and actor.is_member(self.get_id())
                for actor in self.user_actors
            )
        )

    @property
    def user_actors(self):
        return ActorUser.objects.filter(actor_sources__in=self.sources.all())

    def pre_check_obj(self):
        for actor in self.user_actors:
            if not actor.is_member(self.get_id()):
                actor.join_chat(self.get_id())
                self.members.add(actor)

    def check_obj(self):
        try:
            if errors := self._check_users(self.user_actors):
                raise Exception(errors)
        except Exception as e:
            self.errors = str(e)
        else:
            self.errors = None
        finally:
            self.last_check = now()
            self.save()

    def _check_users(self, users: list[ActorUser]):
        errors = [
            f"{user} is not member of {self}"
            for user in users
            if not user.is_member(self.get_id())
        ]
        if errors:
            return errors
        for user in users:
            user.check_obj()
        errors.extend(f"{user} is not active" for user in users if not user.is_active)
        if errors:
            return errors
        errors.extend(f"{user} has errors" for user in users if user.errors)
        if errors:
            return errors
        errors.extend(f"{user} is not ready" for user in users if not user.is_ready)
        if errors:
            return errors
