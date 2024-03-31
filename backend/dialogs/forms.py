from dal import autocomplete
from django.forms import ModelForm, Textarea

from .models import Message, Role, Scene, Dialog


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
            "reply_to_msg": autocomplete.ModelSelect2(
                url="reply_to_msg-autocomplete", forward=["dialog"]
            ),
            "text": Textarea(attrs={"rows": 4, "cols": 70}),
        }


class SceneAdminForm(ModelForm):
    class Meta:
        model = Scene
        fields = "__all__"
        widgets = {
            "telegram_group": autocomplete.ModelSelect2(
                url="telegram_group-autocomplete"
            ),
            "dialog": autocomplete.ModelSelect2(
                url="dialog-autocomplete", forward=["telegram_group"]
            ),
        }


class DialogAdminForm(ModelForm):
    class Meta:
        model = Dialog
        fields = "__all__"
        widgets = {
            "tags": autocomplete.TaggitSelect2(url="tag-autocomplete"),
        }
