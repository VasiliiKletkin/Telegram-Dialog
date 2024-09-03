from django.contrib import admin, messages

from .models import TelegramUserImport
from .tasks import convert_to_orm


class TelegramUserImportAdmin(admin.ModelAdmin):
    actions = ['convert']

    def convert(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Converting to ORM...')
        for obj in queryset:
            convert_to_orm.delay(obj.id)
    convert.short_description = "Convert to ORM"


admin.site.register(TelegramUserImport, TelegramUserImportAdmin)
