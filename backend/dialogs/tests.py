# from django.test import TestCase
# from dialogs.models import Scene, Dialog
# from telegram.models import TelegramGroup, TelegramUser
# from .models import App, ClientSession
# from proxies.models import ProxyServer


# class SceneTestCase(TestCase):
#     def setUp(self) -> None:
#         group = TelegramGroup.objects.create(name="name", username="username")
#         dialog = Dialog.objects.create(name="name_of_dialog")
#         self.scene = Scene.objects.create(dialog=dialog, group=group)

#         client_session = ClientSession.objects.create(name="client_session")
#         app = App.objects.create(api_id="api_id", api_hash="api_hash")

#         self.proxy_server = ProxyServer.objects.create(
#             protocol="protocol", address="address", port=8000, username="username", password="password")

#         self.telegram_user = TelegramUser.objects.create(
#             id=1, app=app, client_session=client_session, proxy_server=self.proxy_server)
#         return super().setUp()

#     def test_check_is_not_ready_with_is_active_false(self):
#         self.scene.is_active = False
#         self.scene.save()
#         self.assertEqual(self.scene.is_ready, False)

#     def test_check_is_ready_with_is_active_true(self):
#         self.scene.is_active = True
#         self.scene.save()
#         self.assertEqual(self.scene.is_ready, True)

#     def test_check_is_not_ready_with_inactive_user(self):
#         self.scene.is_active = True
#         self.scene.save()
#         self.telegram_user.is_active = False
#         self.telegram_user.save()
#         self.assertEqual(self.scene.is_ready, True)

#     def test_check_is_not_ready_with_inactive_proxy(self):
#         self.scene.is_active = True
#         self.scene.save()
#         self.telegram_user.is_active = True
#         self.telegram_user.save()
#         self.telegram_user.proxy_server.is_active = False
#         self.telegram_user.proxy_server.save()
#         self.assertEqual(self.scene.is_ready, True)
        
    