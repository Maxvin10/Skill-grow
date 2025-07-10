from aiogram import Bot, Dispatcher
import asyncio
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from config import TOKEN
from handlers import router
bot = Bot(token = TOKEN)
dp = Dispatcher()



@dp.message(Command("help"))
async def helper(message: Message):
    await message.answer("Bot ma'lumotlari:\n/start - ishga tushirish\n/help - yordam")

async def main():
    dp.include_router(router) #routerni chaqirib olish
    await bot.set_my_commands([
        BotCommand(command = "/start", description="Botni ishga tushirish"),
        BotCommand(command = "/help", description="Yordam")

    ])
    
    await dp.start_polling(bot, polling_timeout=1)


if __name__ == "__main__":
    asyncio.run(main())
