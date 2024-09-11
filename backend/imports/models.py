import json
from django.db import models
from django.db import transaction


from djelethon.models import App, ClientSession
from djelethon.sessions import DjangoSession
from telegram_users.models import TelegramUser
from telegram_clients.models import TelegramClient
from telethon.sessions import SQLiteSession


class TelegramUserImport(models.Model):
    json_field = models.FileField(upload_to="telegram_json")
    session_file = models.FileField(upload_to="telegram_session")

    def __str__(self):
        return f"{self.id}"

    @transaction.atomic
    def convert_to_orm(self):
        json_data = json.loads(self.json_field.read())
        app, app_is_created = App.objects.get_or_create(
            api_id=str(json_data["app_id"]), api_hash=str(json_data["app_hash"])
        )
        client_session, cs_is_created = ClientSession.objects.get_or_create(
            name=json_data["id"],
        )

        user, created = TelegramUser.objects.get_or_create(
            id=json_data["id"],
            defaults={
                "username": json_data.get("username"),
                "first_name": json_data.get("first_name"),
                "last_name": json_data.get("last_name"),
                "lang_code": json_data.get("lang_code"),
                "phone": json_data.get("phone"),
                "sex": json_data.get("sex"),
            },
        )

        TelegramClient.objects.get_or_create(
            user=user,
            defaults={
                "two_fa": json_data["twoFA"],
                "app": app,
                "session": client_session,
            },
        )

        sql_session = SQLiteSession(self.session_file.path)
        django_session = DjangoSession(client_session=client_session)
        django_session.set_dc(
            sql_session.dc_id, sql_session.server_address, sql_session.port
        )
        django_session.auth_key = sql_session.auth_key
