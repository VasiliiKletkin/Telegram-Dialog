from django.urls import path

from .views import MessageRoleNameAutocomplete, DialogMessageAutocomplete, DialogAutocomplete

urlpatterns = [
    path(
        "message_role_name-autocomplete/",
        MessageRoleNameAutocomplete.as_view(),
        name="message_role_name-autocomplete",
    ),
    path(
        "reply_to_msg-autocomplete/",
        DialogMessageAutocomplete.as_view(),
        name="reply_to_msg-autocomplete",
    ),
    path(
        "dialog-autocomplete/",
        DialogAutocomplete.as_view(),
        name="dialog-autocomplete",
    ),
]
