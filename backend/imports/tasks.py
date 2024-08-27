import json

from core.celery import app
from django_telethon.sessions import DjangoSession
from telegram.models import TelegramUser
from telethon.sessions import SQLiteSession, StringSession
from telethon.sync import TelegramClient
from telegram.models import TelegramClient as TC


from .models import TelegramUserImport


@app.task
def convert_to_orm(id):
    tui = TelegramUserImport.objects.get(id=id)
    json_data = json.loads(tui.json_field.read())


    client = TelegramClient(SQLiteSession(tui.session_file.path), api_id, api_hash)
    session_string = StringSession.save(client_session=client.session)

    TelegramUser.objects.get_or_create(
        id=json_data["id"],
        defaults={
            "username": json_data.get("username"),
            "first_name": json_data.get("first_name"),
            "last_name": json_data.get("last_name"),
            "phone": json_data.get("phone"),
            'sex': json_data.get("sex"),
        },
    )

    api_id = int(json_data["app_id"])
    api_hash = str(json_data["app_hash"])
    
    # TC.objects.get_or_create(
    #         "api_id": api_id,
    #         "api_hash": api_hash,   
    #         "two_fa": json_data["twoFA"],
    #         "app_json": json_data,
    #         "app": app,
    #         "session": session_string,
    # )
