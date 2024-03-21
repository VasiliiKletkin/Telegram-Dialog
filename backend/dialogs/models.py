from django.db import models
from model_utils.models import TimeStampedModel
from telegram.models import TelegramGroup, TelegramUser

ROLES = (
    (1, "Role 1"),
    (2, "Role 2"),
    (3, "Role 3"),
    (4, "Role 4"),
    (5, "Role 5"),
    (6, "Role 6"),
    (7, "Role 7"),
    (8, "Role 8"),
    (9, "Role 9"),
    (10, "Role 10"),
    (11, "Role 11"),
    (12, "Role 12"),
    (13, "Role 13"),
    (14, "Role 14"),
    (15, "Role 15"),
    (16, "Role 16"),
    (17, "Role 17"),
    (18, "Role 18"),
    (19, "Role 19"),
    (20, "Role 20"),
)


class Dialog(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.get_roles_count()} roles"

    def get_roles_count(self):
        return self.messages.values("role").distinct().count()


class Message(TimeStampedModel):
    dialog = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.PositiveBigIntegerField()
    text = models.TextField()
    # time = models.TimeField()
    reply_to_msg = models.ForeignKey(
        "Message", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id}:{self.role}: {self.text[:10]}"


class Scene(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="scenes")
    telegram_group = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.dialog.name} {self.telegram_group.username}"

    @property
    def is_ready(self):
        roles = self.roles.all()
        telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()
        are_users_active = all(user.is_ready for user in telegram_users)
        # добавить проверку что все юзеры в чате
        return (
            are_users_active
            and roles.count() == self.dialog.get_roles_count()
            and self.is_active
        )


class Role(TimeStampedModel):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="roles")
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="roles"
    )
    role = models.PositiveBigIntegerField(choices=ROLES)

    def __str__(self):
        return f"{self.telegram_user.username} {self.role}"

    class Meta:
        unique_together = ("scene", "telegram_user", "role")
