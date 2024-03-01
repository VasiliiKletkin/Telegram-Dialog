from typing import Any
from django.contrib import admin
from .tasks import convert
from .models import TelegramUserUpload

# Register your models here.


class TelegramUserUploadAdmin(admin.ModelAdmin):
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        convert(obj.id)


admin.site.register(TelegramUserUpload, TelegramUserUploadAdmin)
