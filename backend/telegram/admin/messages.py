from rangefilter.filters import DateTimeRangeFilter
from django.contrib import admin, messages

from ..models.messages import TelegramGroupMessage


@admin.register(TelegramGroupMessage)
class TelegramGroupMessageAdmin(admin.ModelAdmin):
    search_fields = ("text", "user_id")
    ordering = ("-date",)
    list_display = ("__str__", "user_id", "message_id", "reply_to_msg_id", "date")
    list_filter = [
        ("date", DateTimeRangeFilter),
    ]
