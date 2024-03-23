from django.contrib import admin, messages
from .models import Dialog, Message, Scene, Role
from .tasks import start_scene, check_scene
from .forms import RoleInlineAdminForm, MessageInlineAdminForm, SceneAdminForm
from dal_admin_filters import AutocompleteFilter


class MessageInlineAdmin(admin.TabularInline):
    form = MessageInlineAdminForm
    model = Message
    extra = 1


class DialogAdmin(admin.ModelAdmin):
    inlines = [MessageInlineAdmin]


class RoleInlineAdmin(admin.TabularInline):
    form = RoleInlineAdminForm
    model = Role
    extra = 1


class DialogFilterAdmin(AutocompleteFilter):
    title = "Dialog"
    field_name = "dialog"
    autocomplete_url = "dialog-autocomplete"


class TelegramGroupFilterAdmin(AutocompleteFilter):
    title = "Telegram Group"
    field_name = "telegram_group"
    autocomplete_url = "telegram_group-autocomplete"


# class TelegramUserFilterAdmin(AutocompleteFilter):
#     title = "Telegram User"
#     field_name = "telegram_user"
#     autocomplete_url = "telegram_user-autocomplete"


class SceneAdmin(admin.ModelAdmin):
    list_display = (
        "dialog",
        "telegram_group",
        "roles_count",
        "start_date",
        "is_active",
    )
    search_fields = ["dialog__name", "telegram_group__username"]
    ordering = ["-start_date"]
    list_filter = [
        ("is_active", admin.BooleanFieldListFilter),
        (DialogFilterAdmin),
        (TelegramGroupFilterAdmin),
        # (TelegramUserFilterAdmin),
        ("start_date", admin.DateFieldListFilter),
    ]
    inlines = [RoleInlineAdmin]
    actions = ["start", "check_obj"]
    form = SceneAdminForm

    def start(self, request, queryset):
        messages.add_message(request, messages.INFO, "Scenes starting...")
        for obj in queryset:
            start_scene.delay(obj.id)

    start.short_description = "Start scene"

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Scenes checking...")
        for obj in queryset:
            check_scene.delay(obj.id)

    check_obj.short_description = "Check scene"


admin.site.register(Scene, SceneAdmin)
admin.site.register(Dialog, DialogAdmin)
