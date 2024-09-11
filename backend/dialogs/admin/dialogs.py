from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilter

from ..forms import DialogMessageInlineAdminForm
from ..models import Dialog, DialogMessage


class MessageInlineAdmin(admin.TabularInline):
    form = DialogMessageInlineAdminForm
    model = DialogMessage
    extra = 1
    ordering = ["delay"]


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    inlines = [MessageInlineAdmin]
    list_display = [
        "name",
        "roles_count",
        "messages_count",
        "created",
        "is_active",
    ]
    ordering = [
        "-created",
    ]
    search_fields = [
        "name",
        "id",
    ]
    list_filter = [
        ("is_active", admin.BooleanFieldListFilter),
        ("created", DateTimeRangeFilter),
        # TelegramGroupFilterAdmin,
    ]

    actions = [
        "generate_scenes",
    ]

    # def generate_scenes(self, request, queryset):
    #     messages.add_message(request, messages.INFO, "Generate scenes ...")
    #     for obj in queryset:
    #         generate_scenes_from_dialog(obj.id)

    # generate_scenes.short_description = "Generate scenes"
