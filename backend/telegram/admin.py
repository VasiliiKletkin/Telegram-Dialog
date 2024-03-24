from django.contrib import admin, messages

from .models import TelegramGroup, TelegramUser, TelegramGroupMessage
from .tasks import (
    check_user,
    get_messages_from_group,
    generate_dialogs_from_group,
    save_all_dialogs_from_user,
)


class TelegramGroupAdmin(admin.ModelAdmin):
    actions = ["get_messages", "generate_dialogs"]
    # list_display = ("__str__")

    def get_messages(self, request, queryset):
        messages.add_message(request, messages.INFO, "Parse messages from group...")
        for obj in queryset:
            get_messages_from_group.delay(obj.id)

    get_messages.short_description = "Parse messages"

    def generate_dialogs(self, request, queryset):
        messages.add_message(request, messages.INFO, "Generate dialogs from group...")
        for obj in queryset:
            generate_dialogs_from_group.delay(obj.id)

    generate_dialogs.short_description = "Generate dialogs"


class TelegramUserAdmin(admin.ModelAdmin):
    actions = ["check_obj", "save_all_dialogs"]
    list_display = (
        "__str__",
        "is_active",
        "is_ready",
    )

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Checking...")
        for obj in queryset:
            check_user.delay(obj.id)

    check_obj.short_description = "Check User"

    def save_all_dialogs(self, request, queryset):
        messages.add_message(request, messages.INFO, "Save all dialogs...")
        for obj in queryset:
            save_all_dialogs_from_user.delay(obj.id)

    save_all_dialogs.short_description = "Save all dialogs"


class TelegramGroupMessageAdmin(admin.ModelAdmin):
    search_fields = ("text", "reply_to_msg_id")
    ordering = ("-date",)


admin.site.register(TelegramGroupMessage, TelegramGroupMessageAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramGroup, TelegramGroupAdmin)
