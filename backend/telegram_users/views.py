from dal import autocomplete
from telegram_groups.models import TelegramGroupSource
from .models import ActorUser, MemberUser


class MemberAutocomplete(autocomplete.Select2QuerySetView):
    search_fields = ["username", "id"]

    def get_queryset(self):
        if group_id := self.forwarded.get("group"):
            group = TelegramGroupSource.objects.get(id=group_id)
            return group.members.all()
        return []


class ActorAutocomplete(autocomplete.Select2QuerySetView):
    search_fields = ["username", "id"]
    queryset = ActorUser.active.all()
