from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

qosh = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='oddiy'),
        ],
        [
            KeyboardButton(text='duti')
        ]
    ],
    resize_keyboard=True
)