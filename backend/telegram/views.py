from dal import autocomplete
from django.db.models import Q
from taggit.models import Tag

from .models import TelegramGroup, TelegramUser


class TelegramUserAutocomplete(autocomplete.Select2QuerySetView):
    queryset = TelegramUser.objects.all()
    search_fields = ["username", "first_name", "last_name", "id"]


class TelegramGroupAutocomplete(autocomplete.Select2QuerySetView):
    queryset = TelegramGroup.objects.all()
    search_fields = ["name", "username", "id"]
    
    def get_queryset(self):
        qs = super().get_queryset()

        is_active = self.forwarded.get("is_active")
        if is_active is not None:
            qs = qs.filter(is_active=is_active)
            
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(username__icontains=self.q))
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    queryset = Tag.objects.all()
    search_fields = ["name"]
