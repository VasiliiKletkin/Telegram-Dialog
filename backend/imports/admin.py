from django.contrib import admin, messages
from .tasks import convert
from .models import TelegramUserUpload


class TelegramUserUploadAdmin(admin.ModelAdmin):
    actions = ['convert_to_orm']

    def convert_to_orm(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Scenes started')
        for obj in queryset:
            convert(obj.id)

    convert_to_orm.short_description = "Convert to ORM"


admin.site.register(TelegramUserUpload, TelegramUserUploadAdmin)
