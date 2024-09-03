from typing import Any

from dal_admin_filters import AutocompleteFilter
from django.contrib import admin, messages
from rangefilter.filters import DateTimeRangeFilter
from ..models import TelegramUser

from ..forms import TelegramGroupAdminForm, TelegramUserAdminForm
# from ..tasks import (
#     check_user,
#     generate_dialogs_from_group,
#     save_dialogs_from_user,
#     save_messages_from_group,
# )


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass
    # actions = ["check_obj", "save_all_dialogs"]
    # list_filter = [
    #     ("is_active", admin.BooleanFieldListFilter),
    #     ("created", DateTimeRangeFilter),
    # ]
    # list_display = (
    #     "__str__",
    #     "created",
    # )
    # form = TelegramUserAdminForm

    # def check_obj(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Checking...")
    #     for obj in queryset:
    #         check_user.delay(obj.id)

    # check_obj.short_description = "Check User"

    # def save_all_dialogs(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Save all dialogs...")
    #     for obj in queryset:
    #         save_dialogs_from_user.delay(obj.id)

    # save_all_dialogs.short_description = "Save all dialogs"
