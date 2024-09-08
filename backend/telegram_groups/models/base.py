from django.db import models
from .groups import TelegramGroup

from abc import abstractmethod


class BaseGroupModel(TelegramGroup):
    is_active = models.BooleanField(default=True)
    errors = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_ready(self):
        return self.is_active and not self.errors

    @abstractmethod
    def check_obj(self):
        raise NotImplementedError("check_obj method must be implemented")
