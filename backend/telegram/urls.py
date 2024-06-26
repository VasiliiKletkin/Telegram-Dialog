from django.urls import path

from .views import TelegramUserAutocomplete, TelegramGroupAutocomplete, TagAutocomplete

urlpatterns = [
    path(
        "telegram_user-autocomplete/",
        TelegramUserAutocomplete.as_view(),
        name="telegram_user-autocomplete",
    ),
    path(
        "telegram_group-autocomplete/",
        TelegramGroupAutocomplete.as_view(),
        name="telegram_group-autocomplete",
    ),
    path(
        "tag-autocomplete/",
        TagAutocomplete.as_view(),
        name="tag-autocomplete",
    ),
]
