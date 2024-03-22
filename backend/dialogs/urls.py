from django.urls import path

from .views import MessageRoleNameAutocomplete

urlpatterns = [
    path(
        "message_role_name-autocomplete/",
        MessageRoleNameAutocomplete.as_view(),
        name="message_role_name-autocomplete",
    ),
]
