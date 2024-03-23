import json

from core.celery import app
from django_telethon.models import App, ClientSession
from django_telethon.sessions import DjangoSession
from telegram.models import TelegramUser
from telethon.sessions import SQLiteSession

from .models import TelegramUserImport


@app.task
def convert_to_orm(id):
    tup = TelegramUserImport.objects.get(id=id)
    json_data = json.loads(tup.json_field.read())

    app, app_is_created = App.objects.get_or_create(
        api_id=str(json_data['app_id']),
        api_hash=str(json_data['app_hash'])
    )

    client_session, cs_is_created = ClientSession.objects.get_or_create(
        name=json_data["id"],
    )

    TelegramUser.objects.get_or_create(
        id=json_data['id'],
        defaults={
            'username': json_data.get('username'),
            'first_name': json_data.get('first_name'),
            'last_name': json_data.get('last_name'),
            'phone': json_data.get("phone"),
            'sex': json_data.get("sex"),
            'two_fa': json_data["twoFA"],
            'app_json': json_data,
            'app': app,
            'client_session': client_session,
        }
    )

    sql_session = SQLiteSession(tup.session_file.path)
    django_session = DjangoSession(client_session=client_session)
    django_session.set_dc(
        sql_session.dc_id, sql_session.server_address, sql_session.port)
    django_session.auth_key = sql_session.auth_key
