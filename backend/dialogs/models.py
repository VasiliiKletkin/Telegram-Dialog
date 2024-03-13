from django.db import models
from model_utils.models import TimeStampedModel
from telegram.models import TelegramGroup, TelegramUser


ROLES = (
    (1, 'role-1'),
    (2, 'role-2'),
    (3, 'role-3'),
    (4, 'role-4'),
    (5, 'role-5'),
    (6, 'role-6'),
    (7, 'role-7'),
    (8, 'role-8'),
    (9, 'role-9'),
    (10, 'role-10'),
    (11, 'role-11'),
    (12, 'role-12'),
    (13, 'role-13'),
    (14, 'role-14'),
    (15, 'role-15'),
    (16, 'role-16'),
    (17, 'role-17'),
    (18, 'role-18'),
    (19, 'role-19'),
    (20, 'role-20'),
)


class Dialog(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.get_roles_count()} roles"

    def get_roles_count(self):
        return self.messages.values('role').distinct().count()


class Message(TimeStampedModel):
    dialog = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name='messages')
    role = models.PositiveIntegerField(choices=ROLES)
    text = models.TextField()

    def __str__(self):
        return self.text


class Scene(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    dialog = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name='scenes')
    group = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dialog.name} {self.group.username}"

    @property
    def is_ready(self):
        roles = self.roles.all()
        telegram_users = TelegramUser.objects.filter(roles__in=roles).distinct()
        are_users_active = all(user.is_ready for user in telegram_users)
        return are_users_active and roles.count() == self.dialog.get_roles_count() and self.is_active


class Role(TimeStampedModel):
    scene = models.ForeignKey(
        Scene, on_delete=models.CASCADE, related_name='roles')
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name='roles')
    role = models.PositiveIntegerField(choices=ROLES)

    def __str__(self):
        return f"{self.telegram_user.username} {self.role}"

    class Meta():
        unique_together = ('scene', 'telegram_user', 'role')
