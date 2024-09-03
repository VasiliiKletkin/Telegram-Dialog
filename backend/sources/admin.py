from django.contrib import admin

from .models import TelegramGroupSource, TelegramGroupRole


class TelegramGroupRoleInlineAdmin(admin.TabularInline):
    model = TelegramGroupRole
    extra = 1


@admin.register(TelegramGroupSource)
class TelegramGroupSourceAdmin(admin.ModelAdmin):
    inlines = [TelegramGroupRoleInlineAdmin]
