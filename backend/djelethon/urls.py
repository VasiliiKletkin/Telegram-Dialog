from django.urls import path

from .apps import DjTelethonConfig
from .views import login_bot_view, login_user_view, send_code_request_view

app_name = DjTelethonConfig.name

urlpatterns = [
    path("send-code-request/", send_code_request_view, name="send_code_request"),
    path("login-user-request/", login_user_view, name="login_user_request"),
    path("login-bot-request/", login_bot_view, name="login_bot_request"),
]
