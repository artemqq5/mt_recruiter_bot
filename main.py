import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from commands_.commands_menu import set_menu_commands, cancel_state
from constants_.commands_constant import *
from data_.repository import MyRepository
from private import TELEGRAM_TOKEN_BOT
from constants_.main_constants import HELLO_TEXT, FAQ_INFO
from states.states_vacancy import AddVacancyState

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    if MyRepository().get_user(message.chat.id) is None:  # register user if not registered
        MyRepository().add_user(telegram_id=message.chat.id, username=message.chat.username, role="user")

    await message.answer(HELLO_TEXT, parse_mode=ParseMode.HTML, reply_markup=set_menu_commands(message))


@dp.message_handler(commands=['help'])
async def help_(message: types.Message):
    if MyRepository().get_user(message.chat.id) is not None:  # show bot FAQ info
        await message.answer(FAQ_INFO, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Виникла помилка, перезапустіть бот /start")


@dp.message_handler(commands=['menu'])
async def menu_(message: types.Message):
    if MyRepository().get_user(message.chat.id) is not None:
        await bot.send_message(message.chat.id, "Головне Меню", reply_markup=set_menu_commands(message))
    else:
        await message.answer("Виникла помилка, перезапустіть бот /start")


@dp.message_handler(lambda m: m.text == "Скасувати операцію", state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.reset_state()
    await message.reply('Операцію скасовано', reply_markup=set_menu_commands(message))


# @dp.message_handler(commands=['vacancies'])
# async def vacancies_(message):
#     keyboard_markup = InlineKeyboardMarkup()
#     keyboard_markup.add(InlineKeyboardButton('Зв\'язок', callback_data='link_recruiter'))
#     vacancies = MyRepository().all_vacancies_sql()
#     if vacancies is not None:
#         if vacancies.__sizeof__() > 0:
#             for i in vacancies:
#                 await message.answer(i['title'] + "\n\n" + i['desc'], reply_markup=keyboard_markup)
#         else:
#             await message.answer("Список поки пустий, чекайте на оновлення")
#     else:
#         await message.answer("Помилка при отриманні даних")
#         print("error vacancies")


@dp.message_handler(
    lambda m: m.text in (
            ADD_VACANCY, DELETE_VACANCY, PUBLISHED_VACANCIES_LIST, SEND_MAIL_TO_ALL, LIST_OF_USERS_RESUME,
            SHOW_VACANCIES, CREATE_RESUME))
async def echo(message: types.Message):
    if MyRepository().get_user(message.chat.id) is not None:
        if ADD_VACANCY == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'admin':
                await AddVacancyState.title.set()
                await message.answer("Введіть назву вакансії:", reply_markup=cancel_state())
        elif DELETE_VACANCY == message.text:
            print(DELETE_VACANCY)
        elif PUBLISHED_VACANCIES_LIST == message.text:
            print(PUBLISHED_VACANCIES_LIST)
        elif SEND_MAIL_TO_ALL == message.text:
            print(SEND_MAIL_TO_ALL)
        elif LIST_OF_USERS_RESUME == message.text:
            print(LIST_OF_USERS_RESUME)
        elif SHOW_VACANCIES == message.text:
            print(SHOW_VACANCIES)
        elif CREATE_RESUME == message.text:
            print(CREATE_RESUME)
    else:
        await message.answer("Виникла помилка, перезапустіть бот /start")


@dp.message_handler(content_types=["text"], state=AddVacancyState.title)
async def set_tittle_vacancy(message, state: FSMContext):
    await AddVacancyState.next()
    await state.update_data(title=message.text)
    await message.answer("Введіть вимоги вакансії:", reply_markup=cancel_state())


@dp.message_handler(content_types=["text"], state=AddVacancyState.requirements)
async def set_requirements_vacancy(message, state: FSMContext):
    await AddVacancyState.next()
    await state.update_data(requirements=message.text)
    await message.answer("Введіть обов'зки вакансії:", reply_markup=cancel_state())


@dp.message_handler(content_types=["text"], state=AddVacancyState.responsibilities)
async def set_responsibilities_vacancy(message, state: FSMContext):
    await AddVacancyState.next()
    await state.update_data(responsibilities=message.text)
    await message.answer("Введіть бонуси вакансії:", reply_markup=cancel_state())


@dp.message_handler(content_types=["text"], state=AddVacancyState.bonus)
async def set_bonus_vacancy(message, state: FSMContext):
    await AddVacancyState.next()
    await state.update_data(bonus=message.text)
    await message.answer("Введіть контакти для зв'язку:", reply_markup=cancel_state())


@dp.message_handler(content_types=["text"], state=AddVacancyState.contact)
async def set_contact_vacancy(message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    await state.finish()

    description = (f"<b>Назва:</b> {data['title']}\n\n \
   <b>Вимоги:</b> {data['requirements']}\n\n \
   <b>Обов`зки:</b> {data['responsibilities']}\n\n \
   <b>Що ми пропонуємо:</b> {data['bonus']}\n\n \
   <b>Контакти:</b> {data['contact']}")

    result = MyRepository().add_vacancy(data['title'].replace("'", "''"), description)
    if result is not None:
        await message.answer(f"<b>Вакансію №{result} створено</b>\n\n\n{description}", parse_mode=ParseMode.HTML)
    else:
        await message.answer("Виникла помилка, перезапустіть бот /start")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
