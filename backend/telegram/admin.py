from typing import Any

from dal_admin_filters import AutocompleteFilter
from django.contrib import admin, messages
from rangefilter.filters import DateTimeRangeFilter

from .forms import TelegramGroupAdminForm, TelegramUserAdminForm
from .models import TelegramGroup, TelegramGroupMessage, TelegramUser
from .tasks import (
    check_user,
    generate_dialogs_from_group,
    save_dialogs_from_user,
    save_messages_from_group,
)


class TagFilter(AutocompleteFilter):
    title = "Tags"
    field_name = "tags"
    autocomplete_url = "tag-autocomplete"
    is_placeholder_title = True


class TelegramGroupAdmin(admin.ModelAdmin):
    form = TelegramGroupAdminForm
    actions = ["get_messages", "generate_dialogs"]
    list_display = ("name", "username", "created", "is_active")
    list_filter = [
        "is_active",
        TagFilter,
    ]
    ordering = ["is_active"]

    def save_messages(self, request, queryset):
        messages.add_message(request, messages.INFO, "Parse messages from group...")
        for obj in queryset:
            save_messages_from_group.delay(obj.id)

    save_messages.short_description = "Parse messages"

    def generate_dialogs(self, request, queryset):
        messages.add_message(request, messages.INFO, "Generate dialogs from group...")
        for obj in queryset:
            generate_dialogs_from_group.delay(obj.id)

    generate_dialogs.short_description = "Generate dialogs"


class TelegramGroupFilterAdmin(AutocompleteFilter):
    title = "Telegram Group"
    field_name = "telegram_groups"
    autocomplete_url = "telegram_group-autocomplete"


class TelegramUserAdmin(admin.ModelAdmin):
    actions = ["check_obj", "save_all_dialogs"]
    list_filter = [
        ("is_active", admin.BooleanFieldListFilter),
        "sex",
        ("created", DateTimeRangeFilter),
    ]
    list_display = (
        "__str__",
        "is_active",
        "sex",
        "created",
        "is_ready",
    )
    form = TelegramUserAdminForm

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Checking...")
        for obj in queryset:
            check_user.delay(obj.id)

    check_obj.short_description = "Check User"

    def save_all_dialogs(self, request, queryset):
        messages.add_message(request, messages.INFO, "Save all dialogs...")
        for obj in queryset:
            save_dialogs_from_user.delay(obj.id)

    save_all_dialogs.short_description = "Save all dialogs"


class TelegramGroupMessageAdmin(admin.ModelAdmin):
    search_fields = ("text", "user_id")
    ordering = ("-date",)
    list_display = ("__str__", "user_id", "message_id", "reply_to_msg_id", "date")
    list_filter = [
        ("date", DateTimeRangeFilter),
    ]


admin.site.register(TelegramGroupMessage, TelegramGroupMessageAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramGroup, TelegramGroupAdmin)
