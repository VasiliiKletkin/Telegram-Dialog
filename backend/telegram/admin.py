from django.contrib import admin, messages
from .tasks import send_message
from django.conf import settings
from .models import TelegramGroup, TelegramUser


class TelegramGroupAdmin(admin.ModelAdmin):
    pass


class TelegramUserAdmin(admin.ModelAdmin):
    def send_test_message(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Scenes started')
        for obj in queryset:
            send_message.delay(obj.id, settings.TEST_USER_ID, "This user is working...")

    send_test_message.short_description = "Send test message"


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramGroup, TelegramGroupAdmin)
