from django.contrib import admin, messages
from .tasks import convert_to_orm
from .models import TelegramUserUpload


class TelegramUserUploadAdmin(admin.ModelAdmin):
    actions = ['convert']

    def convert(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Scenes started')
        for obj in queryset:
            convert_to_orm.delay(obj.id)

    convert.short_description = "Convert to ORM"


admin.site.register(TelegramUserUpload, TelegramUserUploadAdmin)
