from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

web = ReplyKeyboardMarkup(
    keyboard = [
    [
        KeyboardButton(text = "Backend"),
        KeyboardButton(text = "Frontend")
    ],
    [
        KeyboardButton(text = "✍️Qo'llanma")
    ]
],
    resize_keyboard=True,
    one_time_keyboard = True
)