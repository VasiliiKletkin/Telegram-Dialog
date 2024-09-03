from django.contrib import admin, messages

from ..forms import TelegramGroupAdminForm
from ..models import TelegramGroup
# from ..tasks import (
#     generate_dialogs_from_group,
#     save_messages_from_group,
# )


@admin.register(TelegramGroup)
class TelegramGroupAdmin(admin.ModelAdmin):
    # form = TelegramGroupAdminForm
    # actions = ["get_messages", "generate_dialogs"]
    list_display = ("name", "groupname", "created",)


    # def save_messages(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Parse messages from group...")
    #     for obj in queryset:
    #         save_messages_from_group.delay(obj.id)

    # save_messages.short_description = "Parse messages"

    # def generate_dialogs(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Generate dialogs from group...")
    #     for obj in queryset:
    #         generate_dialogs_from_group.delay(obj.id)

    # generate_dialogs.short_description = "Generate dialogs"


# from typing import Any

# from dal_admin_filters import AutocompleteFilter
# from django.contrib import admin, messages
# from rangefilter.filters import DateTimeRangeFilter

# from .forms import TelegramGroupAdminForm, TelegramUserAdminForm
# from .models import (
#     TelegramGroup,
#     TelegramGroupMessage,
#     TelegramUser,
#     ListenerTelegramGroup,
# )
# from .tasks import (
#     check_user,
#     generate_dialogs_from_group,
#     save_dialogs_from_user,
#     save_messages_from_group,
# )


# class TagFilter(AutocompleteFilter):
#     title = "Tags"
#     field_name = "tags"
#     autocomplete_url = "tag-autocomplete"
#     is_placeholder_title = True


# class TelegramGroupFilterAdmin(AutocompleteFilter):
#     title = "Telegram Group"
#     field_name = "telegram_groups"
#     autocomplete_url = "telegram_group-autocomplete"
