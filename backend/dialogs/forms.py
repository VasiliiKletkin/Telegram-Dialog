from dal import autocomplete, forward
from django import forms

from .models import DialogMessage, SceneRole, Scene


class SceneRoleInlineAdminForm(forms.ModelForm):
    name = autocomplete.Select2ListChoiceField(
        choice_list=DialogMessage.objects.values_list(
            "role_name",
            "role_name",
        ).distinct(),
        widget=autocomplete.ListSelect2(
            url="message_role_name-autocomplete", forward=["dialog"]
        ),
    )

    class Meta:
        model = SceneRole
        fields = "__all__"
        widgets = {
            "actor": autocomplete.ModelSelect2(
                url="actor-autocomplete",
                forward=[forward.Field("drain", "drain_id")],
            ),
        }


class DialogMessageInlineAdminForm(forms.ModelForm):
    class Meta:
        model = DialogMessage
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
            "drain": autocomplete.ModelSelect2(url="drain-autocomplete"),
            "dialog": autocomplete.ModelSelect2(
                url="dialog-autocomplete",
                forward=["telegram_group", forward.Const(True, "is_active")],
            ),
        }
