from django.urls import path

from .views import TelegramGroupDrainAutocomplete, TelegramGroupSourceAutocomplete

urlpatterns = [
    path(
        "drain-autocomplete/",
        TelegramGroupDrainAutocomplete.as_view(),
        name="drain-autocomplete",
    ),
    path(
        "source-autocomplete/",
        TelegramGroupSourceAutocomplete.as_view(),
        name="source-autocomplete",
    ),
]
