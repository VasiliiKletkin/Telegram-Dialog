from django.contrib import admin, messages

from .models import TelegramUserUpload
from .tasks import convert_to_orm


class TelegramUserUploadAdmin(admin.ModelAdmin):
    actions = ['convert']

    def convert(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Converting...')
        for obj in queryset:
            convert_to_orm.delay(obj.id)
    convert.short_description = "Convert to ORM"


admin.site.register(TelegramUserUpload, TelegramUserUploadAdmin)
