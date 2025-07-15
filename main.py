from aiogram import Bot, Dispatcher
import asyncio
import logging
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from config import TOKEN
from handlers.handlers import router
from handlers.ai import ai_router
bot = Bot(token = TOKEN)
dp = Dispatcher()



@dp.message(Command("help"))
async def helper(message: Message):
    await message.answer("Bot ma'lumotlari:\n/start - ishga tushirish\n/help - yordam")

async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router) #routerni chaqirib olish
    dp.include_router(ai_router)
    await bot.set_my_commands([
        BotCommand(command = "/start", description="Botni ishga tushirish"),
        BotCommand(command = "/help", description="Yordam"),
        BotCommand(command = "/menu", description = "Menular")

    ])
    
    await dp.start_polling(bot, polling_timeout=1, skip_updates = True)


if __name__ == "__main__":
    asyncio.run(main())
