from dal import autocomplete

from .models import ProxyServer


class ProxyAutocomplete(autocomplete.Select2QuerySetView):
    queryset = ProxyServer.objects.filter(is_active=True, telegram_user__isnull=True)
    search_fields = ["address", "username", "id"]
