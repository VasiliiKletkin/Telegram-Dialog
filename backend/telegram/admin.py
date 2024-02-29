from typing import Any
from django.contrib import admin
from .models import TelegramGroup, TelegramUser, TelegramUserUpload
from .tasks import convert


class TelegramGroupAdmin(admin.ModelAdmin):
    pass


class TelegramUserAdmin(admin.ModelAdmin):
    pass


class TelegramUserUploadAdmin(admin.ModelAdmin):
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        convert.delay(obj.id)


admin.site.register(TelegramUserUpload, TelegramUserUploadAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramGroup, TelegramGroupAdmin)
