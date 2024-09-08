from djelethon.sessions import DjangoSession
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from asgiref.sync import async_to_sync


@async_to_sync
async def get_dialogs(client: TelegramClient):
    dialogs = []
    async with client:
        dialogs = await client.get_dialogs(limit=200)
    return dialogs


@async_to_sync
async def get_me(client: TelegramClient):
    # await client.start(
    #     phone=telegram_user.phone, password=telegram_user.two_fa
    # )
    me = None
    async with client:
        me = await client.get_me()
    return me


@async_to_sync
async def send_message(client: TelegramClient, chat_id, text, reply_to_msg_id=None):
    async with client:
        entity = await client.get_entity(chat_id)
        return await client.send_message(
            entity=entity,
            message=text,
            reply_to=reply_to_msg_id,
        )


@async_to_sync
async def get_messages(client: TelegramClient, chat_id, limit=1000):
    messages = []
    async with client:
        entity = await client.get_entity(chat_id)
        messages = await client.get_messages(entity, limit=limit)
    return messages


@async_to_sync
async def join_chat(client: TelegramClient, chat_id):
    async with client:
        chat = await client.get_entity(chat_id)
        await client(JoinChannelRequest(chat))


@async_to_sync
async def get_participants(client: TelegramClient, chat_id: int):
    async with client:
        chat = await client.get_entity(chat_id)
        return await client.get_participants(chat)
