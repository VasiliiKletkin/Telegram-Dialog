from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from asgiref.sync import async_to_sync


@async_to_sync
async def get_dialogs(client_session, api_id, api_hash, proxy_dict):
    telegram_client = TelegramClient(
        session=StringSession(client_session=client_session),
        api_id=api_id,
        api_hash=api_hash,
        proxy=proxy_dict,
    )
    dialogs = []
    async with telegram_client:
        dialogs = await telegram_client.get_dialogs(limit=200)
    return dialogs


@async_to_sync
async def get_me(client_session, api_id, api_hash, proxy_dict):
    telegram_client = TelegramClient(
        session=StringSession(client_session=client_session),
        api_id=api_id,
        api_hash=api_hash,
        proxy=proxy_dict,
    )
    # await telegram_client.start(
    #     phone=telegram_user.phone, password=telegram_user.two_fa
    # )
    me = None
    async with telegram_client:
        me = await telegram_client.get_me()
    return me


@async_to_sync
async def send_message(
    client_session,
    api_id,
    api_hash,
    proxy_dict,
    username,
    text,
    reply_to_msg_id=None,
):
    telegram_client = TelegramClient(
        session=StringSession(client_session=client_session),
        api_id=api_id,
        api_hash=api_hash,
        proxy=proxy_dict,
    )
    message = None
    async with telegram_client:
        chat = await telegram_client.get_entity(username)
        message = await telegram_client.send_message(
            chat,
            text,
            reply_to=reply_to_msg_id,
        )
    return message


@async_to_sync
async def get_messages(client_session, api_id, api_hash, proxy_dict, username):
    telegram_client = TelegramClient(
        session=StringSession(client_session=client_session),
        api_id=api_id,
        api_hash=api_hash,
        proxy=proxy_dict,
    )
    messages = []
    async with telegram_client:
        entity = await telegram_client.get_entity(username)
        messages = await telegram_client.get_messages(entity, limit=1000)
    return messages


@async_to_sync
async def join_to_chat(client_session, api_id, api_hash, proxy_dict, chat_id):
    telegram_client = TelegramClient(
        session=StringSession(client_session=client_session),
        api_id=api_id,
        api_hash=api_hash,
        proxy=proxy_dict,
    )
    async with telegram_client:
        chat = await telegram_client.get_entity(chat_id)
        await telegram_client(JoinChannelRequest(chat))


THEMES = {
    ("документы", "документ"): "Документы",
}


def get_tags_from_str(text):
    tags = []
    for word in text.split():
        for theme in THEMES:
            if word.lower() in theme:
                tags.append(THEMES[theme])
    return tags
