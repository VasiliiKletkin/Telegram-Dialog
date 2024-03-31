from dal import autocomplete
from django.db.models import Q

from .models import Message, Dialog, Scene


class MessageRoleNameAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        qs = Message.objects.values_list("id", "role_name").distinct()

        if dialog := self.forwarded.get("dialog", None):
            qs = qs.filter(dialog=dialog)

        if self.q:
            qs = qs.filter(Q(role__icontains=self.q))
        return qs


class MessageAutocomplete(autocomplete.Select2QuerySetView):
    queryset = Message.objects.all()
    search_fields = ["text", "id"]


class DialogAutocomplete(autocomplete.Select2QuerySetView):
    queryset = Dialog.objects.all()
    search_fields = ["name", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        if is_active := self.forwarded.get("is_active"):
            qs = qs.filter(is_active=is_active)

        if telegram_group := self.forwarded.get("telegram_group"):
            scenes = Scene.objects.filter(telegram_group=telegram_group)
            qs = qs.exclude(scenes__in=scenes)
        return qs
