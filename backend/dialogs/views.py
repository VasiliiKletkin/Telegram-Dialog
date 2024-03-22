from dal import autocomplete
from django.db.models import Q

from .models import Message, Dialog


class MessageRoleNameAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        qs = Message.objects.all()

        if dialog := self.forwarded.get("dialog", None):
            qs = qs.filter(dialog=dialog)

        if self.q:
            qs = qs.filter(Q(role__icontains=self.q))
        return qs.values_list("role_name", flat=True).distinct()


class MessageAutocomplete(autocomplete.Select2QuerySetView):
    queryset = Message.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class DialogAutocomplete(autocomplete.Select2QuerySetView):
    queryset = Dialog.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
