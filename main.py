import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from commands_.commands_menu import set_menu_commands, cancel_state
from commands_.vacancy_ import add_vacancy_cmd_, show_vacancies_cmd, end_vacancy, delete_vacancies_cmd
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


@dp.message_handler(
    lambda m: m.text in (
            ADD_VACANCY, DELETE_VACANCY, SEND_MAIL_TO_ALL, LIST_OF_USERS_RESUME, SHOW_VACANCIES, CREATE_RESUME))
async def echo_commands(message: types.Message):
    if MyRepository().get_user(message.chat.id) is not None:
        if ADD_VACANCY == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'admin':
                await add_vacancy_cmd_(message)
        elif DELETE_VACANCY == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'admin':
                await delete_vacancies_cmd(message)
        elif SEND_MAIL_TO_ALL == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'admin':
                await message.answer("У розробці")
        elif LIST_OF_USERS_RESUME == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'admin':
                await message.answer("У розробці")
        elif SHOW_VACANCIES == message.text:
            await show_vacancies_cmd(message)
        elif CREATE_RESUME == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'user':
                await message.answer("У розробці")
    else:
        await message.answer("Виникла помилка, перезапустіть бот /start")


@dp.message_handler(state=AddVacancyState.title)
async def set_tittle_vacancy(message: types.Message, state: FSMContext):
    await AddVacancyState.next()
    await state.update_data(title=message.text)
    await message.answer("Введіть вимоги вакансії:", reply_markup=cancel_state())


@dp.message_handler(state=AddVacancyState.requirements)
async def set_requirements_vacancy(message: types.Message, state: FSMContext):
    await AddVacancyState.next()
    await state.update_data(requirements=message.text)
    await message.answer("Введіть обов'зки вакансії:", reply_markup=cancel_state())


@dp.message_handler(state=AddVacancyState.responsibilities)
async def set_responsibilities_vacancy(message: types.Message, state: FSMContext):
    await AddVacancyState.next()
    await state.update_data(responsibilities=message.text)
    await message.answer("Введіть що ми пропонуємо:", reply_markup=cancel_state())


@dp.message_handler(state=AddVacancyState.bonus)
async def set_bonus_vacancy(message: types.Message, state: FSMContext):
    await AddVacancyState.next()
    await state.update_data(bonus=message.text)
    await message.answer("Введіть контакти для зв'язку:", reply_markup=cancel_state())


@dp.message_handler(state=AddVacancyState.contact)
async def set_contact_vacancy(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    await state.finish()
    await end_vacancy(message, data)


@dp.callback_query_handler(lambda call: "vacancy" in call.data)
async def callback_handlers(call):
    vacancy = MyRepository().get_vacancy(call.data.split("_")[1])

    if vacancy is not None:
        link_button = InlineKeyboardMarkup()
        link_button.add(InlineKeyboardButton(text="Зв'язатися з рекрутером", url=f"https://t.me/{vacancy['contact']}"))

        if MyRepository().get_user(call.message.chat.id)['role'] == 'admin':
            link_button.add(InlineKeyboardButton(text="Видалити", callback_data=f"delete_{vacancy['id']}"))

        vacancy_desc = (f"{vacancy['title']}\n\n\n"
                        f"<b>Вимоги</b>\n{vacancy['requirements']}\n\n"
                        f"<b>Обов`зки\n</b>{vacancy['responsibilities']}\n\n"
                        f"<b>Що ми пропонуємо</b>\n{vacancy['bonus']}\n\n")
        await call.message.answer(text=vacancy_desc, parse_mode=ParseMode.HTML, reply_markup=link_button)
    else:
        await call.message.answer("Вакансії вже не існує")


@dp.callback_query_handler(lambda call: "delete" in call.data)
async def callback_handlers(call):
    vacancy = MyRepository().get_vacancy(call.data.split("_")[1])
    if vacancy is not None:
        if MyRepository().delete_vacancy(vacancy['id']) is not None:
            await call.message.answer("Вакансію успішно видалено")
        else:
            await call.message.answer("Помилка при видаленні")
    else:
        await call.message.answer("Вакансії вже не існує")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
