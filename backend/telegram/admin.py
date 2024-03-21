from django.contrib import admin, messages

from .models import TelegramGroup, TelegramUser, TelegramGroupMessage
from .tasks import check_user, get_messages_from_group


class TelegramGroupAdmin(admin.ModelAdmin):
    actions = ["get_messages"]
    # list_display = ("__str__")

    def get_messages(self, request, queryset):
        messages.add_message(request, messages.INFO, "Parse messages from group...")
        for obj in queryset:
            get_messages_from_group(obj.id)

    get_messages.short_description = "Parse messages"


class TelegramUserAdmin(admin.ModelAdmin):
    actions = ["check_obj"]
    list_display = ("__str__", "is_active")

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Checking...")
        for obj in queryset:
            check_user.delay(obj.id)

    check_obj.short_description = "Check User"


class TelegramGroupMessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(TelegramGroupMessage, TelegramGroupMessageAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramGroup, TelegramGroupAdmin)
