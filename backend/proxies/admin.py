from django.contrib import admin, messages

from proxies.models import ProxyServer


class ProxyServerAdmin(admin.ModelAdmin):
    actions = ["check_obj"]
    list_display = (
        "__str__",
        "created",
        "is_active",
        "is_ready",
    )

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Checking...")
        for obj in queryset:
            obj.check_obj()

    check_obj.short_description = "Check Proxy"


admin.site.register(ProxyServer, ProxyServerAdmin)
