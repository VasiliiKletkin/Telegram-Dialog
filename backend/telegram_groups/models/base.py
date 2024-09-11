from django.db import models
from .groups import TelegramGroup

from abc import abstractmethod


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseGroupModel(TelegramGroup):
    is_active = models.BooleanField(default=False)
    last_check = models.DateTimeField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)

    active = ActiveManager()

    class Meta:
        abstract = True

    @property
    def is_ready(self):
        return self.is_active and not self.errors and bool(self.last_check)

    @abstractmethod
    def check_obj(self):
        raise NotImplementedError("check_obj method must be implemented")

    @abstractmethod
    def pre_check_obj(self):
        raise NotImplementedError("pre_check_obj method must be implemented")