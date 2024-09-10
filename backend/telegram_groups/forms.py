from django import forms
from roles.models import TelegramGroupRole
from dal import autocomplete


class TelegramGroupRoleAdminForm(forms.ModelForm):
    class Meta:
        model = TelegramGroupRole
        fields = "__all__"
        widgets = {
            "member": autocomplete.ModelSelect2(
                url="member-autocomplete",
                forward=[
                    "source",
                ],
            ),
            "actor": autocomplete.ModelSelect2(
                url="actor-autocomplete",
                forward=[
                    "source",
                ],
            ),
        }
