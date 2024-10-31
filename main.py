from aiogram import Bot, Dispatcher
import asyncio
import logging
import app.db as db
from decouple import config
from app.ha1 import router

TOKEN = config('TOKEN', cast=str)
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    logging.basicConfig(level=logging.INFO)
    db.create_table()
    dp.include_router(router)
    await dp.start_polling(bot)
    db.conn.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")