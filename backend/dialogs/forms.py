from dal import autocomplete
from django.forms import ModelForm

from .models import Role, Message, Scene


class RoleInlineAdminForm(ModelForm):
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


class MessageInlineAdminForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        widgets = {
            "reply_to_msg": autocomplete.ListSelect2(url="reply_to_msg-autocomplete"),
        }


class SceneAdminForm(ModelForm):
    class Meta:
        model = Scene
        fields = "__all__"
        widgets = {
            "dialog": autocomplete.ModelSelect2(
                url="dialog-autocomplete",
            ),
            "telegram_group": autocomplete.ModelSelect2(
                url="telegram_group-autocomplete"
            ),
        }
