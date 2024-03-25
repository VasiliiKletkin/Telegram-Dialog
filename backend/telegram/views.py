from dal import autocomplete
from django.db.models import Q

from .models import TelegramUser, TelegramGroup


class TelegramUserAutocomplete(autocomplete.Select2QuerySetView):
    queryset = TelegramUser.objects.all()
    search_fields = ["username", "first_name", "last_name", "id"]


class TelegramGroupAutocomplete(autocomplete.Select2QuerySetView):
    queryset = TelegramGroup.objects.filter(is_active=True)
    search_fields = ["name", "username", "id"]
