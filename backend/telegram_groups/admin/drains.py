from ..models import TelegramGroupDrain
from django.contrib import admin, messages
from .base import BaseTelegramGroupModelAdmin


@admin.register(TelegramGroupDrain)
class TelegramGroupDrainAdmin(BaseTelegramGroupModelAdmin):
    actions = [
        "save_messages",
        "save_members",
    ] + BaseTelegramGroupModelAdmin.actions
