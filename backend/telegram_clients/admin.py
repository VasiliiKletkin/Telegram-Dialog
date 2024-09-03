from django.contrib import admin

from .models import TelegramClient


@admin.register(TelegramClient)
class TelegramClientAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "is_active", "is_ready")
    list_filter = ("is_active",)
    search_fields = ("phone", "two_fa")
