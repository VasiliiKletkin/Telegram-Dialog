from dal import autocomplete
from django.db.models import Q

from .models import DialogMessage, Dialog, Scene


class MessageRoleNameAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        qs = (
            DialogMessage.objects.all().values_list("role_name", "role_name").distinct()
        )
        if dialog := self.forwarded.get("dialog", None):
            qs = qs.filter(dialog=dialog)
            if self.q:
                qs = qs.filter(Q(role_name__icontains=self.q))
            return qs
        return []


class MessageAutocomplete(autocomplete.Select2QuerySetView):
    queryset = DialogMessage.objects.all()
    search_fields = ["text", "id"]


class DialogAutocomplete(autocomplete.Select2QuerySetView):
    queryset = Dialog.objects.all()
    search_fields = ["name", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        is_active = self.forwarded.get("is_active")

        if is_active is not None:
            qs = qs.filter(is_active=is_active)

        if telegram_group := self.forwarded.get("telegram_group"):
            scenes = Scene.objects.filter(telegram_group=telegram_group)
            qs = qs.exclude(scenes__in=scenes)
        return qs
