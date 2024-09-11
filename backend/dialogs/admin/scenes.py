from dal_admin_filters import AutocompleteFilter
from django.contrib import admin, messages
from rangefilter.filters import DateTimeRangeFilter

from ..forms import (
    SceneRoleInlineAdminForm,
    SceneAdminForm,
)
from ..models import SceneRole, Scene


# class DialogFilterAdmin(AutocompleteFilter):
#     title = "Dialog"
#     field_name = "dialog"
#     autocomplete_url = "dialog-autocomplete"


# class TelegramGroupFilterAdmin(AutocompleteFilter):
#     title = "Telegram Group"
#     field_name = "telegram_group"
#     autocomplete_url = "telegram_group-autocomplete"


# class TelegramUserFilterAdmin(AutocompleteFilter):
#     title = "Telegram User"
#     field_name = "telegram_user"
#     autocomplete_url = "telegram_user-autocomplete"


# class TagFilter(AutocompleteFilter):
#     title = "Tags"
#     field_name = "tags"
#     autocomplete_url = "tag-autocomplete"
#     is_placeholder_title = True


class SceneRoleInlineAdmin(admin.TabularInline):
    form = SceneRoleInlineAdminForm
    model = SceneRole
    extra = 1


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    inlines = [SceneRoleInlineAdmin]
    form = SceneAdminForm
    list_display = (
        "dialog",
        "drain",
        "start_date",
        "last_check",
        "is_active",
        "is_ready",
    )
    search_fields = [
        "dialog__name",
        "drain__groupname",
        "id",
    ]
    ordering = [
        "-start_date",
    ]
    list_filter = [
        ("is_active", admin.BooleanFieldListFilter),
        # (DialogFilterAdmin),
        # (TelegramGroupFilterAdmin),
        # (TelegramUserFilterAdmin),
        ("start_date", DateTimeRangeFilter),
    ]
    actions = [
        "pre_check_obj",
        "check_obj",
        "start_now",
        "start_on_time",
    ]

    def pre_check_obj(self, request, queryset: list[Scene]):
        messages.add_message(request, messages.INFO, "Pre checking...")
        for obj in queryset:
            obj.pre_check_obj()

    pre_check_obj.short_description = "Pre check"

    def check_obj(self, request, queryset: list[Scene]):
        messages.add_message(request, messages.INFO, "Checking...")
        for obj in queryset:
            obj.check_obj()

    check_obj.short_description = "Check"

    def start_now(self, request, queryset: list[Scene]):
        messages.add_message(request, messages.INFO, "Starting ...")
        for obj in queryset:
            obj.start()

    start_now.short_description = "Start"

    def start_on_time(self, request, queryset: list[Scene]):
        messages.add_message(request, messages.INFO, "Create tasks...")
        for obj in queryset:
            pass
            # (obj.id)

    start_on_time.short_description = "Start on time"
