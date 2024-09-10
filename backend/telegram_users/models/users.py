from django.db import models
from model_utils.models import TimeStampedModel


class TelegramUser(TimeStampedModel):
    FEMALE = 0
    MALE = 1

    SEX_CHOICE = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    lang_code = models.CharField(max_length=8, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    sex = models.PositiveIntegerField(choices=SEX_CHOICE, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["username"], name="username_idx"),
            models.Index(fields=["first_name"], name="first_name_idx"),
            models.Index(fields=["last_name"], name="last_name_idx"),
        ]

    def get_id(self):
        return self.id

    def is_member(self, group_id):
        return self.groups.filter(id=group_id).exists()

    def get_username(self):
        return f"@{self.username}" if self.username else None

    def __str__(self):
        return f"{self.get_id()}-{self.first_name} {self.last_name}-{self.get_username()}"
