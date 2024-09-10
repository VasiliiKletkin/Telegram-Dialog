from django.contrib import admin, messages


class BaseTelegramGroupModelAdmin(admin.ModelAdmin):
    actions = [
        "check_obj",
        "pre_check_obj",
    ]
    list_display = (
        "name",
        "groupname",
        "last_check",
        "is_active",
        "is_ready",
    )

    def pre_check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Pre Checking...")
        for obj in queryset:
            obj.pre_check_obj()

    pre_check_obj.short_description = "Pre Check"

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Checking...")
        for obj in queryset:
            obj.check_obj()

    check_obj.short_description = "Check"
