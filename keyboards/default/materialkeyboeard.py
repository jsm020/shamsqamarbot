from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,WebAppInfo

material = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Laminad'),
            KeyboardButton(text='Krashni'),
        ],
        [
            KeyboardButton(text='Shpon')
        ],
        [
            KeyboardButton(text="calculate",
                               web_app=WebAppInfo(url=f"https://botweb-gk7l.onrender.com/")),
        ],
    ],
    resize_keyboard=True
)