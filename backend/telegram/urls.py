from django.urls import path

from .views import TelegramUserAutocomplete

urlpatterns = [
    path(
        "telegram_user-autocomplete/",
        TelegramUserAutocomplete.as_view(),
        name="telegram_user-autocomplete",
    ),
]
