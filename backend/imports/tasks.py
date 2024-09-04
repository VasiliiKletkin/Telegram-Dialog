import json

from core.celery import app
from djelethon.models import App, ClientSession
from djelethon.sessions import DjangoSession
from telegram.models import TelegramUser
from telegram_clients.models import TelegramClient
from telethon.sessions import SQLiteSession

from .models import TelegramUserImport


@app.task
def convert_to_orm(import_id):
    tui = TelegramUserImport.objects.get(id=import_id)
    json_data = json.loads(tui.json_field.read())

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

    sql_session = SQLiteSession(tui.session_file.path)
    django_session = DjangoSession(client_session=client_session)
    django_session.set_dc(
        sql_session.dc_id, sql_session.server_address, sql_session.port
    )
    django_session.auth_key = sql_session.auth_key
