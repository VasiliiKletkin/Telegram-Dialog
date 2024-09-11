from dal import autocomplete
from .models import TelegramGroupDrain, TelegramGroupSource


class TelegramGroupSourceAutocomplete(autocomplete.Select2QuerySetView):
    queryset = TelegramGroupSource.active.all()
    search_fields = ["name", "groupname", "id"]


class TelegramGroupDrainAutocomplete(autocomplete.Select2QuerySetView):
    queryset = TelegramGroupDrain.active.all()
    search_fields = ["name", "groupname", "id"]
