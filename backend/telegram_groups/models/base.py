from django.db import models

from telegram_users.models.members import MemberUser
from .groups import TelegramGroup
from django.db.models import QuerySet

from abc import abstractmethod


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseGroupModel(models.Model):
    group = models.OneToOneField(TelegramGroup, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    last_check = models.DateTimeField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)

    active = ActiveManager()

    class Meta:
        abstract = True

    @property
    def is_ready(self) -> bool:
        return self.is_active and not self.errors and bool(self.last_check)

    @property
    def members(self) -> QuerySet[MemberUser]:
        return self.group.members

    @property
    def groupname(self) -> str:
        return self.group.groupname

    @property
    def name(self) -> str:
        return self.group.name

    @property
    def messages(self) -> QuerySet:
        return self.group.messages

    @abstractmethod
    def check_obj(self):
        raise NotImplementedError("check_obj method must be implemented")

    @abstractmethod
    def pre_check_obj(self):
        raise NotImplementedError("pre_check_obj method must be implemented")

    def get_id(self):
        return self.group.get_id()

    def get_messages_count(self):
        return self.group.get_messages_count()

    def get_groupname(self):
        return self.group.get_groupname()

    def __str__(self):
        return str(self.group)
