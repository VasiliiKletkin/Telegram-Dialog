from django.urls import path

from .views import ProxyAutocomplete

urlpatterns = [
    path(
        "proxy_server-autocomplete/",
        ProxyAutocomplete.as_view(),
        name="proxy_server-autocomplete",
    ),
]
