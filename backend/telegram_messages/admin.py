from rangefilter.filters import DateTimeRangeFilter
from django.contrib import admin, messages

from .models import TelegramGroupMessage


@admin.register(TelegramGroupMessage)
class TelegramGroupMessageAdmin(admin.ModelAdmin):
    search_fields = ("text", "user_id")
    ordering = ("-date",)
    list_display = ("get_short_text", "user_id", "message_id", "reply_to_msg", "date", "group")
    list_filter = [
        ("date", DateTimeRangeFilter),
    ]
