import random
from typing import Any

from dal import autocomplete, forward
from django import forms
from telegram.models import TelegramUser

from .models import Dialog, Message, Role, Scene


class RoleInlineAdminForm(forms.ModelForm):
    name = autocomplete.Select2ListChoiceField(
        choice_list=Message.objects.values_list("id", "role_name").distinct(),
        widget=autocomplete.ListSelect2(
            url="message_role_name-autocomplete", forward=["dialog"]
        ),
    )

    class Meta:
        model = Role
        fields = "__all__"
        widgets = {
            # "name": autocomplete.ListSelect2(
            #     url="message_role_name-autocomplete", forward=["dialog"]
            # ),
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

    def save(self, commit: bool) -> Any:
        scene = super().save()
        if scene.roles_count < scene.dialog.roles_count:
            for _ in range(scene.dialog.roles_count - scene.roles_count):
                available_users_id = (
                    TelegramUser.objects.filter(is_active=True)
                    .exclude(
                        id__in=scene.roles.values_list("telegram_user_id", flat=True)
                    )
                    .values_list("id", flat=True)
                )

                available_name_roles = (
                    scene.dialog.messages.exclude(
                        role_name__in=scene.roles.values_list("name", flat=True)
                    )
                    .values_list("role_name", flat=True)
                    .distinct()
                )

                scene.roles.create(
                    telegram_user_id=random.choice(available_users_id),
                    name=random.choice(available_name_roles),
                )


class DialogAdminForm(forms.ModelForm):
    class Meta:
        model = Dialog
        fields = "__all__"
        widgets = {
            "tags": autocomplete.TaggitSelect2(url="tag-autocomplete"),
        }
