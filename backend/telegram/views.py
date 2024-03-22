from dal import autocomplete
from django.db.models import Q

from .models import TelegramUser, TelegramGroup


class TelegramUserAutocomplete(autocomplete.Select2QuerySetView):
    queryset = TelegramUser.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
                | Q(id__icontains=self.q)
            )
        return qs


class TelegramGroupAutocomplete(autocomplete.Select2QuerySetView):
    queryset = TelegramGroup.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(username__icontains=self.q))
        return qs
