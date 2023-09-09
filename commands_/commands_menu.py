from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from constants_.commands_constant import *
from data_.repository import MyRepository


def set_menu_commands(message) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if MyRepository().get_user(message.chat.id)['role'] == 'admin':
        keyboard.add(
            KeyboardButton(ADD_VACANCY),
            KeyboardButton(DELETE_VACANCY),
            KeyboardButton(SEND_MAIL_TO_ALL),
            KeyboardButton(LIST_OF_USERS_RESUME),
            KeyboardButton(SHOW_VACANCIES),
        )
    else:
        keyboard.add(
            KeyboardButton(CREATE_RESUME),
            KeyboardButton(SHOW_VACANCIES),
        )

    return keyboard


def cancel_state() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Скасувати операцію")]], resize_keyboard=True)
