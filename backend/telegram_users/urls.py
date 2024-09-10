from django.urls import path

from telegram_users.views import MemberAutocomplete, ActorAutocomplete


urlpatterns = [
    path(
        "member-autocomplete/",
        MemberAutocomplete.as_view(),
        name="member-autocomplete",
    ),
    path(
        "actor-autocomplete/",
        ActorAutocomplete.as_view(),
        name="actor-autocomplete",
    ),
]
