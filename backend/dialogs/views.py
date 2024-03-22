from dal import autocomplete
from django.db.models import Q

from .models import Message


class MessageRoleNameAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        qs = Message.objects.all()

        if dialog := self.forwarded.get("dialog", None):
            qs = qs.filter(dialog=dialog)

        if self.q:
            qs = qs.filter(Q(role__icontains=self.q))
        return qs.values_list("role", flat=True).distinct()
