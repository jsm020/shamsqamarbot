from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

nalichnik = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='nalichnik 8sm'),
            KeyboardButton(text='nalichnik 10sm'),
        ],
        [
            KeyboardButton(text='nalichnik 16mm')
        ]
    ],
    resize_keyboard=True
)

nalichnik2 = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='nalichnik 8sm'),
        ],
        [
            KeyboardButton(text='nalichnik 10sm'),
        ]
    ],
    resize_keyboard=True
)