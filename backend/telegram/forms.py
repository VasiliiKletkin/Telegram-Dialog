from django.forms import ModelForm
from dal import autocomplete, forward

from .models import TelegramGroup, TelegramUser


class TelegramGroupAdminForm(ModelForm):
    class Meta:
        model = TelegramGroup
        fields = "__all__"
        widgets = {
            "tags": autocomplete.TaggitSelect2(url="tag-autocomplete"),
            "similar_groups": autocomplete.ModelSelect2Multiple(url="telegram_group-autocomplete",
                                                                forward=[forward.Const(False, "is_active"),]
                                                                )
        }

