from django.contrib import admin, messages

from .models import TelegramGroupSource
from roles.models import TelegramGroupRole
from .tasks import save_messages_from_group

class TelegramGroupRoleInlineAdmin(admin.TabularInline):
    model = TelegramGroupRole
    extra = 1


@admin.register(TelegramGroupSource)
class TelegramGroupSourceAdmin(admin.ModelAdmin):
    inlines = [TelegramGroupRoleInlineAdmin]
    actions = ["save_messages", "generate_dialogs"]
    list_display = (
        "name",
        "groupname",
        "created",
    )

    def save_messages(self, request, queryset):
        messages.add_message(request, messages.INFO, "Saving messages...")
        for obj in queryset:
            save_messages_from_group.delay(obj.id)

    save_messages.short_description = "Save messages from group"

    # def generate_dialogs(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Generate dialogs from group...")
    #     for obj in queryset:
    #         generate_dialogs_from_group.delay(obj.id)

    # generate_dialogs.short_description = "Generate dialogs"
