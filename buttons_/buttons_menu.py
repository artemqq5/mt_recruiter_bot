from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from constants_.commands_constant import *
from data_.repository import MyRepository


def set_menu_commands(message) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    if MyRepository().get_user(message.chat.id)['role'] == 'admin':
        keyboard.add(KeyboardButton(ADD_VACANCY))
        keyboard.add(KeyboardButton(SHOW_VACANCIES))
        keyboard.add(KeyboardButton(SEND_MAIL_TO_ALL))
        keyboard.add(KeyboardButton(LIST_OF_USERS_RESUME))
    else:
        keyboard.add(KeyboardButton(MY_RESUME))
        keyboard.add(KeyboardButton(CREATE_RESUME))
        keyboard.add(KeyboardButton(SHOW_VACANCIES))

    return keyboard


def cancel_state() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Скасувати операцію")]], resize_keyboard=True)


def workflow_type() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    keyboard.add(KeyboardButton("Удаленка"))
    keyboard.add(KeyboardButton("Офіс"))
    keyboard.add(KeyboardButton("Гибрид"))
    keyboard.add(KeyboardButton("Скасувати операцію"))

    return keyboard


def source_type() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    keyboard.add(KeyboardButton("Google"))
    keyboard.add(KeyboardButton("FB"))
    keyboard.add(KeyboardButton("Tik Tok"))
    keyboard.add(KeyboardButton("Push"))
    keyboard.add(KeyboardButton("In - app"))
    keyboard.add(KeyboardButton("SEO"))
    keyboard.add(KeyboardButton("Тизерні мережі"))
    keyboard.add(KeyboardButton("Скасувати операцію"))

    return keyboard


def verticals_type() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    keyboard.add(KeyboardButton("Gambling"))
    keyboard.add(KeyboardButton("Betting"))
    keyboard.add(KeyboardButton("Другое"))
    keyboard.add(KeyboardButton("Скасувати операцію"))

    return keyboard


def geo_type() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    keyboard.add(KeyboardButton("Tier-1"))
    keyboard.add(KeyboardButton("Tier-2"))
    keyboard.add(KeyboardButton("Tier-3"))
    keyboard.add(KeyboardButton("Скасувати операцію"))

    return keyboard
