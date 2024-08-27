import random

from django.db import models
from model_utils.models import TimeStampedModel
from proxies.models import ProxyServer


class TelegramUser(
    TimeStampedModel,
):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["username"], name="username_idx"),
            models.Index(fields=["first_name"], name="first_name_idx"),
            models.Index(fields=["last_name"], name="last_name_idx"),
        ]

    def get_group_count(self):
        return self.telegram_groups.count()

    def get_username(self):
        return f"@{self.username}" if self.username else None

    def __str__(self):
        return f"id:{self.id}-{self.get_username()}"


class TelegramClient(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    api_id = models.PositiveIntegerField()
    api_hash = models.CharField(max_length=255)
    session = models.TextField()
    app_json = models.JSONField()

    phone = models.CharField(max_length=30)
    two_fa = models.CharField(max_length=30)

    telegram_user = models.OneToOneField(
        TelegramUser, on_delete=models.CASCADE, related_name="telegram_client"
    )
    proxy_server = models.OneToOneField(
        ProxyServer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="telegram_client",
    )

    error = models.TextField(null=True, blank=True)

    @property
    def is_ready(self):
        return (
            (self.proxy_server.is_ready and self.is_active and not self.error)
            if self.proxy_server
            else False
        )

    def __str__(self):
        return f"{self.telegram_user.id} - @{self.telegram_user.username} - {self.telegram_user.first_name}  {self.telegram_user.last_name}"

    @classmethod
    def get_random(cls, include_ids=None, exclude_ids=None):
        qs = cls.objects.filter(is_active=True)
        if include_ids:
            qs = qs.filter(id__in=include_ids)
        if exclude_ids:
            qs = qs.exclude(id__in=exclude_ids)
        ids = qs.values_list("id", flat=True)
        return cls.objects.get(id=random.choice(ids))


class TelegramGroup(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    is_listening = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=32, unique=True)
    users = models.ManyToManyField(
        TelegramUser, related_name="telegram_groups", blank=True
    )

    def get_users_count(self):
        return self.users.count()

    def get_username(self):
        return f"@{self.username}"

    def __str__(self):
        return f"{self.name} - {self.get_username()}"


class ListenerTelegramGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_listening=True)


class ListenerTelegramGroup(TelegramGroup):
    objects = ListenerTelegramGroupManager()

    class Meta:
        proxy = True


class TelegramGroupMessage(models.Model):
    telegram_group = models.ForeignKey(
        TelegramGroup, on_delete=models.CASCADE, related_name="messages"
    )
    message_id = models.BigIntegerField()
    text = models.TextField()
    date = models.DateTimeField()
    user_id = models.BigIntegerField(
        null=True,
        blank=True,
    )
    reply_to_msg_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["telegram_group", "message_id"],
                name="unique_telegram_group_message_id",
            )
        ]
        # indexes = [
        #     models.Index(fields=["message_id"], name="message_id_idx"),
        #     models.Index(fields=["telegram_group"], name="telegram_group_idx"),
        #     models.Index(fields=["date"], name="date_idx"),
        #     models.Index(fields=["user_id"], name="user_id_idx"),
        #     models.Index(fields=["reply_to_msg_id"], name="reply_to_msg_id_idx"),
        # ]

    def __str__(self):
        return f"@{self.telegram_group.username} - {self.text[:20]}"

    # FEMALE = 0
    # MALE = 1

    # SEX_CHOICE = (
    #     (MALE, "Male"),
    #     (FEMALE, "Female"),
    # )

    # sex = models.PositiveIntegerField(choices=SEX_CHOICE, null=True, blank=True)
