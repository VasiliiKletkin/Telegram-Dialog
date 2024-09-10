from dal import autocomplete, forward
from django import forms

from .models import Dialog, Message, Role, Scene


class RoleInlineAdminForm(forms.ModelForm):
    name = autocomplete.Select2ListChoiceField(
        choice_list=Message.objects.values_list("role_name", "role_name").distinct(),
        widget=autocomplete.ListSelect2(
            url="message_role_name-autocomplete", forward=["dialog"]
        ),
    )

    class Meta:
        model = Role
        fields = "__all__"
        widgets = {
            "telegram_user": autocomplete.ModelSelect2(
                url="telegram_user-autocomplete"
            ),
        }


class MessageInlineAdminForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        widgets = {
            "reply_to_msg": autocomplete.ModelSelect2(
                url="reply_to_msg-autocomplete", forward=["dialog"]
            ),
            "text": forms.Textarea(attrs={"rows": 4, "cols": 70}),
        }


class SceneAdminForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = "__all__"
        widgets = {
            "telegram_group": autocomplete.ModelSelect2(
                url="telegram_group-autocomplete"
            ),
            "dialog": autocomplete.ModelSelect2(
                url="dialog-autocomplete",
                forward=["telegram_group", forward.Const(True, "is_active")],
            ),
        }

class DialogAdminForm(forms.ModelForm):
    class Meta:
        model = Dialog
        fields = "__all__"
        # widgets = {
        #     "tags": autocomplete.TaggitSelect2(url="tag-autocomplete"),
        # }
