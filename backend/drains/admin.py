from django.contrib import admin

from .models import TelegramGroupDrain


@admin.register(TelegramGroupDrain)
class TelegramGroupDrainAdmin(admin.ModelAdmin):
    pass
