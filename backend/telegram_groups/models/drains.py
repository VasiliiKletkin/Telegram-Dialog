from .base import BaseGroupModel
from django.db import models
from .sources import TelegramGroupSource

# from actors.models import Actors


class TelegramGroupDrain(BaseGroupModel):
    sources = models.ManyToManyField(
        TelegramGroupSource, related_name="drains", blank=True
    )

    def get_actors(self):
        Actors.objects.filter(sources__in=self.sources.all())
        self.sources


    @property
    def is_ready(self):
        for source in self.sources.all():
            for actor in source.actors.all():
                if not actor.is_member(self.id):
                    return False
        return True

    def check_obj(self):
        try:
            errors = ""
            for source in self.sources.all():
                for actor in source.actors.all():
                    if not actor.is_member(self.id):
                        actor.check_obj()
                        errors += f"{actor} is not member of {self},"
            if errors:
                raise Exception(f"Actors:{errors}")
        except Exception as e:
            self.errors = str(e)
        else:
            self.errors = None
        finally:
            self.save()
