from django.contrib import admin, messages

from proxies.models import ProxyServer
from .tasks import check_proxy


class ProxyServerAdmin(admin.ModelAdmin):
    actions = ['check_obj']
    list_display = ("__str__", "is_active")

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Scenes started')
        for obj in queryset:
            check_proxy.delay(obj.id)

    check_obj.short_description = "Check Proxy"


admin.site.register(ProxyServer, ProxyServerAdmin)
