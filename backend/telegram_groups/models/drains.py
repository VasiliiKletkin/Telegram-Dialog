from .base import BaseGroupModel
from django.db import models
from .sources import TelegramGroupSource
from django.utils.timezone import now

from telegram_users.models import ActorUser


class TelegramGroupDrain(BaseGroupModel):
    sources = models.ManyToManyField(
        TelegramGroupSource, related_name="drains", blank=True
    )

    def get_actors(self):
        return ActorUser.objects.filter(actor_sources__in=self.sources.all())

    @property
    def is_ready(self):
        return (
            self.is_active
            and not self.errors
            and bool(self.last_check)
            and self.are_members(self.get_actors())
            and all(actor.is_ready for actor in self.get_actors())
        )

    def pre_check_obj(self):
        for actor in self.get_actors():
            if not actor.is_member(self.id):
                actor.join_chat(self.get_id())
                self.members.add(actor)

    def check_obj(self):
        try:
            errors = ""
            for actor in self.get_actors():
                if not actor.is_member(self.id):
                    errors += f"{actor} is not member of {self}"
            if errors:
                raise Exception(errors)
            for source in self.sources.all():
                source.check_obj()
        except Exception as e:
            self.errors = str(e)
        else:
            self.errors = None
        finally:
            self.last_check = now()
            self.save()
