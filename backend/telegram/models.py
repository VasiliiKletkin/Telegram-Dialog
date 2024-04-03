import random

from django.db import models
from django_telethon.models import App, ClientSession
from model_utils.models import TimeStampedModel
from proxies.models import ProxyServer
from taggit.managers import TaggableManager


class TelegramGroup(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    tags = TaggableManager(blank=True)

    similar_groups = models.ManyToManyField(
        "self",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} - @{self.username}"


class TelegramGroupMessage(models.Model):
    telegram_group = models.ForeignKey(
        TelegramGroup, on_delete=models.CASCADE, related_name="messages"
    )
    message_id = models.BigIntegerField(db_index=True)
    text = models.TextField(db_index=True)
    date = models.DateTimeField()
    user_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    reply_to_msg_id = models.BigIntegerField(null=True, blank=True, db_index=True)

    class Meta:
        unique_together = ("telegram_group", "message_id")

    def __str__(self):
        return f"@{self.telegram_group.username} - {self.text[:20]}"


class TelegramUser(TimeStampedModel):
    FEMALE = 0
    MALE = 1

    SEX_CHOICE = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    is_active = models.BooleanField(default=True)

    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True, db_index=True)
    first_name = models.CharField(
        default="", max_length=64, null=True, blank=True, db_index=True
    )
    last_name = models.CharField(
        default="", max_length=64, null=True, blank=True, db_index=True
    )
    sex = models.PositiveIntegerField(choices=SEX_CHOICE, null=True, blank=True)
    # country = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    two_fa = models.CharField(max_length=30, null=True, blank=True)

    app = models.ForeignKey(App, on_delete=models.CASCADE)
    client_session = models.OneToOneField(ClientSession, on_delete=models.CASCADE)

    proxy_server = models.OneToOneField(
        ProxyServer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="telegram_user",
    )

    telegram_groups = models.ManyToManyField(
        TelegramGroup, related_name="telegram_users", null=True, blank=True
    )
    app_json = models.JSONField(null=True, blank=True)

    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - @{self.username} - {self.first_name}  {self.last_name}"

    @property
    def is_ready(self):
        return (
            (self.proxy_server.is_ready and self.is_active and not self.error)
            if self.proxy_server
            else False
        )

    def is_member_of_group(self, username):
        return self.telegram_groups.filter(username=username).exists()

    @classmethod
    def get_random(cls, include_ids=None, exclude_ids=None):
        qs = cls.objects.filter(is_active=True)
        if include_ids:
            qs = qs.filter(id__in=include_ids)
        if exclude_ids:
            qs = qs.exclude(id__in=exclude_ids)
        ids = qs.values_list("id", flat=True)
        return cls.objects.get(id=random.choice(ids))
