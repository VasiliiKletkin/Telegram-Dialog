from dal import autocomplete
from django.db.models import Q

from .models import TelegramUser


class TelegramUserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = TelegramUser.objects.all()
        return qs
