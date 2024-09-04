from django.forms import ModelForm
from dal import autocomplete, forward

from .models import TelegramClient


class TelegramClientAdminForm(ModelForm):
    class Meta:
        model = TelegramClient
        fields = "__all__"
        widgets = {
            "proxy": autocomplete.ModelSelect2(url="proxy_server-autocomplete"),
        }
