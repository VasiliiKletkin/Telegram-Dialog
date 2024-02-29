from django.contrib import admin

from proxies.models import ProxyServer

class ProxyServerAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProxyServer, ProxyServerAdmin)