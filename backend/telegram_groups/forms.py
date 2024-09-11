from django import forms
from roles.models import TelegramGroupRole
from dal import autocomplete, forward


class TelegramGroupRoleAdminForm(forms.ModelForm):
    class Meta:
        model = TelegramGroupRole
        fields = "__all__"
        widgets = {
            "member": autocomplete.ModelSelect2(
                url="member-autocomplete",
                forward=[forward.Field("source", "group")],
            ),
            "actor": autocomplete.ModelSelect2(
                url="actor-autocomplete",
            ),
        }
