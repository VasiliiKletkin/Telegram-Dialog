from django.forms import ModelForm
from dal import autocomplete

from .models import TelegramGroup


class TelegramGroupAdminForm(ModelForm):
    class Meta:
        model = TelegramGroup
        fields = "__all__"
        widgets = {
            "tags": autocomplete.TaggitSelect2(url="tag-autocomplete"),
        }
