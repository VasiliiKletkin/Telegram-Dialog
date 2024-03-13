from django.test import TestCase
from .models import TelegramUser
from django_telethon.models import App, ClientSession
from proxies.models import ProxyServer


class TelegramUserTestCase(TestCase):
    def setUp(self) -> None:
        client_session = ClientSession.objects.create(name="client_session")
        app = App.objects.create(api_id="api_id", api_hash="api_hash")
        self.telegram_user = TelegramUser.objects.create(
            id=1, is_active=True, app=app, client_session=client_session)

        self.proxy_server = ProxyServer.objects.create(
            is_active=False, protocol="protocol", address="address", port=8000, username="username", password="password")
        return super().setUp()

    def test_check_is_not_ready_without_proxy(self):
        self.assertEqual(self.telegram_user.is_ready, False)

    def test_check_is_not_ready_with_proxy(self):
        self.proxy_server.is_active = False
        self.proxy_server.save()
        self.telegram_user.proxy_server = self.proxy_server
        self.telegram_user.save()
        self.assertEqual(self.telegram_user.is_ready, False)

    def test_check_is_ready(self):
        self.proxy_server.is_active = True
        self.proxy_server.save()        
        self.telegram_user.proxy_server = self.proxy_server
        self.telegram_user.save()
        self.assertEqual(self.telegram_user.is_ready, True)

    def test_check_is_ready_with_inactive(self):
        self.telegram_user.is_active = False
        self.telegram_user.save()
        self.assertEqual(self.telegram_user.is_ready, False)
