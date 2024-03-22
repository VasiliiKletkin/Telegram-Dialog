from dal import autocomplete
from django.forms import ModelForm

from .models import Role


class RoleInlineForm(ModelForm):
    class Meta:
        model = Role
        fields = "__all__"
        widgets = {
            "name": autocomplete.ListSelect2(
                url="message_role_name-autocomplete", forward=["dialog"]
            ),
            "telegram_user": autocomplete.ModelSelect2(
                url="telegram_user-autocomplete"
            ),
        }
