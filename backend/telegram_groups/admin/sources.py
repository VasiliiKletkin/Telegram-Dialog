from typing import List
from django.contrib import admin, messages
from django.utils.timezone import now

from datetime import timedelta

from ..models import TelegramGroupSource
from .base import BaseTelegramGroupModelAdmin


@admin.register(TelegramGroupSource)
class TelegramGroupSourceAdmin(BaseTelegramGroupModelAdmin):
    actions = [
        "save_messages",
        "save_members",
        "generate_dialog",
    ] + BaseTelegramGroupModelAdmin.actions

    def save_messages(self, request, queryset: List[TelegramGroupSource]):
        messages.add_message(request, messages.INFO, "Saving messages...")
        for obj in queryset:
            obj.save_messages()

    save_messages.short_description = "Save messages"

    def save_members(self, request, queryset: List[TelegramGroupSource]):
        messages.add_message(request, messages.INFO, "Saving members...")
        for obj in queryset:
            obj.save_members()

    save_members.short_description = "Save members"

    def generate_dialog(self, request, queryset: List[TelegramGroupSource]):
        messages.add_message(request, messages.INFO, "Testing...")
        for obj in queryset:
            obj.generate_dialog(
                date_from=now() - timedelta(days=1),
                date_to=now(),
            )

    # def generate_dialogs(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Generate dialogs from group...")
    #     for obj in queryset:
    #         generate_dialogs_from_group.delay(obj.id)

    # generate_dialogs.short_description = "Generate dialogs"
