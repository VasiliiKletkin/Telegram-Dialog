from ..models import TelegramGroupDrain
from django.contrib import admin


@admin.register(TelegramGroupDrain)
class TelegramGroupDrainAdmin(admin.ModelAdmin):
    pass
