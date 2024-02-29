from telethon import TelegramClient


async def send_message(chat_id, message, session, api_id, api_hash, proxy=None):
    telegram_client = TelegramClient(
        session=session,
        api_id=api_id,
        api_hash=api_hash,
        proxy=proxy
    )
    async with telegram_client:
        await telegram_client.send_message(chat_id, message)
