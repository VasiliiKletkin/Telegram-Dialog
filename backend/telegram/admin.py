from django.contrib import admin, messages
from .tasks import check_user
from .models import TelegramGroup, TelegramUser


class TelegramGroupAdmin(admin.ModelAdmin):
    pass


class TelegramUserAdmin(admin.ModelAdmin):
    actions = ['check_obj']
    list_display = ("__str__", "is_active")

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Scenes started')
        for obj in queryset:
            check_user(obj.id)

    check_obj.short_description = "Check User"

admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramGroup, TelegramGroupAdmin)
