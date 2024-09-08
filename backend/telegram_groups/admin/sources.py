from django.contrib import admin, messages

from ..models import TelegramGroupSource
from roles.models import TelegramGroupRole

# from tasks import save_messages_from_group


class TelegramGroupRoleInlineAdmin(admin.TabularInline):
    model = TelegramGroupRole
    extra = 1


@admin.register(TelegramGroupSource)
class TelegramGroupSourceAdmin(admin.ModelAdmin):
    inlines = [TelegramGroupRoleInlineAdmin]
    actions = ["save_messages", "check_obj", "pre_check_obj"]
    list_display = (
        "name",
        "groupname",
        "created",
        "is_active",
        "is_ready",
    )

    def pre_check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Pre Check...")
        for obj in queryset:
            obj.pre_check_obj()

    pre_check_obj.short_description = "Pre Check"

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Checking...")
        for obj in queryset:
            obj.check_obj()
    check_obj.short_description = "Check"

    # def save_messages(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Saving messages...")
    #     for obj in queryset:
    #         pass
    #         # save_messages_from_group.delay(obj.id)

    # save_messages.short_description = "Save messages from group"

    # def generate_dialogs(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Generate dialogs from group...")
    #     for obj in queryset:
    #         generate_dialogs_from_group.delay(obj.id)

    # generate_dialogs.short_description = "Generate dialogs"
