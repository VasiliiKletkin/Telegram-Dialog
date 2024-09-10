from djelethon.sessions import DjangoSession
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from asgiref.sync import async_to_sync


@async_to_sync
async def get_dialogs(session, api_hash, api_id, proxy):
    client = TelegramClient(
        session=session, api_hash=api_hash, api_id=api_id, proxy=proxy
    )
    async with client:
        return await client.get_dialogs(limit=200)


@async_to_sync
async def get_me(session, api_hash, api_id, proxy):
    client = TelegramClient(
        session=session, api_hash=api_hash, api_id=api_id, proxy=proxy
    )
    async with client:
        return await client.get_me()


@async_to_sync
async def send_message(
    session, api_hash, api_id, proxy, chat_id, text, reply_to_msg_id=None
):
    client = TelegramClient(
        session=session, api_hash=api_hash, api_id=api_id, proxy=proxy
    )
    async with client:
        entity = await client.get_entity(chat_id)
        return await client.send_message(
            entity=entity,
            message=text,
            reply_to=reply_to_msg_id,
        )


@async_to_sync
async def get_messages(session, api_hash, api_id, proxy, chat_id, limit=1000):
    client = TelegramClient(
        session=session, api_hash=api_hash, api_id=api_id, proxy=proxy
    )
    async with client:
        entity = await client.get_entity(chat_id)
        return await client.get_messages(entity, limit=limit)


@async_to_sync
async def join_chat(session, api_hash, api_id, proxy, chat_id):
    client = TelegramClient(
        session=session, api_hash=api_hash, api_id=api_id, proxy=proxy
    )
    async with client:
        chat = await client.get_entity(chat_id)
        return await client(JoinChannelRequest(chat))


@async_to_sync
async def get_participants(session, api_hash, api_id, proxy, chat_id, limit=1000):
    client = TelegramClient(
        session=session, api_hash=api_hash, api_id=api_id, proxy=proxy
    )
    async with client:
        chat = await client.get_entity(chat_id)
        return await client.get_participants(chat)
