from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ReplyKeyboardRemove

from commands_.commands_menu import cancel_state, set_menu_commands
from data_.repository import MyRepository
from states.states_vacancy import AddVacancyState


async def add_vacancy_cmd_(message):
    await AddVacancyState.title.set()
    await message.answer("Введіть назву вакансії:", reply_markup=cancel_state())


async def show_vacancies_cmd(message):
    vacancies = MyRepository().all_vacancies_sql()
    if vacancies is not None:
        if len(vacancies) > 0:
            keyboard_markup = InlineKeyboardMarkup()
            for i in vacancies:
                keyboard_markup.add(InlineKeyboardButton(i["title"], callback_data=f"vacancy_{i['id']}"))
            await message.answer("Доступні вакансії:", reply_markup=keyboard_markup)
        else:
            await message.answer("Список поки пустий, чекайте на оновлення")
    else:
        await message.answer("Помилка при отриманні даних")
        print("error vacancies")


async def delete_vacancies_cmd(message):
    vacancies = MyRepository().all_vacancies_sql()
    if vacancies is not None:
        if len(vacancies) > 0:
            keyboard_markup = InlineKeyboardMarkup()
            for i in vacancies:
                keyboard_markup.add(InlineKeyboardButton(i["title"], callback_data=f"delete_{i['id']}"))
            await message.answer("Доступні вакансії::", reply_markup=keyboard_markup)
        else:
            await message.answer("Список поки пустий, чекайте на оновлення")
    else:
        await message.answer("Помилка при отриманні даних")
        print("error vacancies")


async def end_vacancy(message, data):

    result = MyRepository().add_vacancy(
        title=data['title'],
        requirements=data['requirements'],
        responsibilities=data['responsibilities'],
        bonus=data['bonus'],
        contact=data['contact']
    )

    if result is not None:
        await message.answer(
            (f"<b>Вакансію #{result} створено</b>\n\n"
             f"<b>Назва</b>\n{data['title']}\n\n"
             f"<b>Вимоги</b>\n{data['requirements']}\n\n"
             f"<b>Обов`зки</b>\n{data['responsibilities']}\n\n"
             f"<b>Що ми пропонуємо</b>\n{data['bonus']}\n\n"
             f"<b>Контакти</b>\n{data['contact']}"),
            parse_mode=ParseMode.HTML,
            reply_markup=set_menu_commands(message))
    else:
        await message.answer("Виникла помилка, перезапустіть бот /start", reply_markup=ReplyKeyboardRemove())
