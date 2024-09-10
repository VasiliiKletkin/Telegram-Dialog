from dal import autocomplete
from telegram_groups.models import TelegramGroupSource
from .models import ActorUser, MemberUser


class MemberAutocomplete(autocomplete.Select2QuerySetView):
    search_fields = ["username", "id"]

    def get_queryset(self):
        if telegram_group := self.forwarded.get("source"):
            source = TelegramGroupSource.objects.get(id=telegram_group)
            return source.members.exclude(
                id__in=source.listeners.values_list(
                    "id",
                    flat=True,
                )
            )
        return []


class ActorAutocomplete(autocomplete.Select2QuerySetView):
    search_fields = ["username", "id"]

    def get_queryset(self):
        if telegram_group := self.forwarded.get("source"):
            source = TelegramGroupSource.objects.get(id=telegram_group)
            return ActorUser.objects.exclude(
                id__in=source.listeners.values_list(
                    "id",
                    flat=True,
                )
            )
        return []
