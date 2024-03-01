import json

from asgiref.sync import async_to_sync
from telegram.models import TelegramUser
from core.celery import app
from django_telethon.models import App, ClientSession
from django_telethon.sessions import DjangoSession
from telethon import TelegramClient
from telethon.sessions import SQLiteSession

from .models import TelegramUserUpload


@app.task
@async_to_sync
async def convert(id):
    tup = TelegramUserUpload.objects.get(id=id)
    json_data = json.loads(tup.json_field.read())

    app, app_is_created = App.objects.update_or_create(
        api_id=str(json_data['app_id']),
        api_hash=str(json_data['app_hash'])
    )

    client_session, cs_is_created = ClientSession.objects.update_or_create(
        name=json_data['session_file'],
    )

    TelegramUser.objects.update_or_create(
        id=json_data['id'],
        defaults={
            'username': json_data['username'],
            'first_name': json_data['first_name'],
            'last_name': json_data['last_name'],
            'app_json': json_data,
            'app': app,
            'session': client_session,
        }
    )

    sql_session = SQLiteSession(tup.session_file.path)
    django_session = DjangoSession(client_session=client_session)
    django_session.set_dc(
        sql_session.dc_id, sql_session.server_address, sql_session.port)
    django_session.auth_key = sql_session.auth_key

    telegram_client = TelegramClient(
        django_session, app.api_id, app.api_hash)