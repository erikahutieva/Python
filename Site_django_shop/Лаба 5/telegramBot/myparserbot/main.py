import asyncio
from config import *
from aiogram import Bot, Dispatcher, types
from handlers.user_private import user_private_Router

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_private_Router)

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())