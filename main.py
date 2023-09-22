import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from buttons_.buttons_menu import set_menu_commands, cancel_state, workflow_type, source_type, verticals_type, \
    geo_type
from commands_.mailing_cmd import mailing_user_cmd, mailing_message_cmd
from commands_.resume_cmd import add_start_resume_cmd, add_finish_resume_cmd, my_resume_cmd, all_resume_cmd
from commands_.vacancy_cmd import add_start_vacancy_cmd, show_vacancies_cmd, add_finish_vacancy_cmd
from constants_.commands_constant import *
from data_.repository import MyRepository
from private import TELEGRAM_TOKEN_BOT
from constants_.main_constants import HELLO_TEXT, FAQ_INFO
from states.mailing_state import MailingState
from states.resume_state import ResumeState
from states.vacancy_state import VacancyState

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
    lambda m: m.text in (ADD_VACANCY, SEND_MAIL_TO_ALL, LIST_OF_USERS_RESUME, SHOW_VACANCIES, CREATE_RESUME, MY_RESUME))
async def echo_commands(message: types.Message):
    if MyRepository().get_user(message.chat.id) is not None:

        if ADD_VACANCY == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'admin':
                await add_start_vacancy_cmd(message)

        elif SEND_MAIL_TO_ALL == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'admin':
                await mailing_message_cmd(message)

        elif LIST_OF_USERS_RESUME == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'admin':
                await all_resume_cmd(message)

        elif SHOW_VACANCIES == message.text:
            await show_vacancies_cmd(message)

        elif CREATE_RESUME == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'user':
                await add_start_resume_cmd(message)

        elif MY_RESUME == message.text:
            if MyRepository().get_user(message.chat.id)['role'] == 'user':
                await my_resume_cmd(bot, message)

    else:
        await message.answer("Виникла помилка, перезапустіть бот /start")


@dp.message_handler(state=MailingState.mailing)
async def mailing_users(message: types.Message, state: FSMContext):
    await state.finish()
    await mailing_user_cmd(bot, message)


@dp.message_handler(state=VacancyState.title)
async def set_tittle_vacancy(message: types.Message, state: FSMContext):
    await VacancyState.next()
    await state.update_data(title=message.text)
    await message.answer("Введіть вимоги вакансії:", reply_markup=cancel_state())


@dp.message_handler(state=VacancyState.requirements)
async def set_requirements_vacancy(message: types.Message, state: FSMContext):
    await VacancyState.next()
    await state.update_data(requirements=message.text)
    await message.answer("Введіть обов'зки вакансії:", reply_markup=cancel_state())


@dp.message_handler(state=VacancyState.responsibilities)
async def set_responsibilities_vacancy(message: types.Message, state: FSMContext):
    await VacancyState.next()
    await state.update_data(responsibilities=message.text)
    await message.answer("Введіть що ми пропонуємо:", reply_markup=cancel_state())


@dp.message_handler(state=VacancyState.bonus)
async def set_bonus_vacancy(message: types.Message, state: FSMContext):
    await VacancyState.next()
    await state.update_data(bonus=message.text)
    await message.answer("Введіть контакти для зв'язку (твій нік тг без @):", reply_markup=cancel_state())


@dp.message_handler(state=VacancyState.contact)
async def set_contact_vacancy(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    await state.finish()
    await add_finish_vacancy_cmd(message, data)


@dp.message_handler(state=ResumeState.name)
async def set_name_resume(message: types.Message, state: FSMContext):
    await ResumeState.next()
    await state.update_data(name=message.text)
    await message.answer("Скільки тобі років?", reply_markup=cancel_state())


@dp.message_handler(lambda message: message.text.isdigit(), state=ResumeState.age)
async def set_age_resume(message: types.Message, state: FSMContext):
    await ResumeState.next()
    await state.update_data(age=message.text)
    await message.answer("Введіть місце проживання:", reply_markup=cancel_state())


@dp.message_handler(lambda message: not message.text.isdigit(), state=ResumeState.age)
async def set_age_wrong_resume(message: types.Message):
    await message.answer("Вік вимірюється в числах, повторіть спробу:", reply_markup=cancel_state())


@dp.message_handler(state=ResumeState.city)
async def set_city_resume(message: types.Message, state: FSMContext):
    await ResumeState.next()
    await state.update_data(city=message.text)
    await message.answer("Який формат роботи тобі підходить?", reply_markup=workflow_type())


@dp.message_handler(state=ResumeState.workflow)
async def set_workflow_resume(message: types.Message, state: FSMContext):
    await ResumeState.next()
    await state.update_data(workflow=message.text)
    await message.answer("З якими джерелами працюєш? Якщо декілька, напиши про це", reply_markup=source_type())


@dp.message_handler(state=ResumeState.sources)
async def set_sources_resume(message: types.Message, state: FSMContext):
    await ResumeState.next()
    await state.update_data(sources=message.text)
    await message.answer("З якими вертикалями працюєш?", reply_markup=verticals_type())


@dp.message_handler(state=ResumeState.verticals)
async def set_verticals_resume(message: types.Message, state: FSMContext):
    await ResumeState.next()
    await state.update_data(verticals=message.text)
    await message.answer("З якими ГЕО ти працюєш?", reply_markup=geo_type())


@dp.message_handler(state=ResumeState.geo)
async def set_geo_resume(message: types.Message, state: FSMContext):
    await ResumeState.next()
    await state.update_data(geo=message.text)
    await message.answer("Які обсяги профіту на місяць?", reply_markup=cancel_state())


@dp.message_handler(state=ResumeState.profit)
async def set_profit_resume(message: types.Message, state: FSMContext):
    await ResumeState.next()
    await state.update_data(profit=message.text)
    await message.answer("Скинь фото статистики останніх заливів (Скинь саме фото, не файлом)",
                         reply_markup=cancel_state())


@dp.message_handler(content_types=["photo"], state=ResumeState.statistic)
async def set_statistic_resume(message: types.Message, state: FSMContext):
    smallest_photo_id = message.photo[0].file_id
    await state.update_data(statistic=smallest_photo_id)
    data = await state.get_data()
    await state.finish()
    await add_finish_resume_cmd(bot, message, data)


@dp.message_handler(lambda message: message.photo == [], state=ResumeState.statistic)
async def set_wrong_statistic_resume(message: types.Message, state: FSMContext):
    await message.answer("Неправильний формат, скинь фото")


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


@dp.callback_query_handler(lambda call: "resume" in call.data)
async def callback_handlers(call):
    user_resume = MyRepository().get_user(call.data.split("_")[1])
    if user_resume is not None:
        link_button = InlineKeyboardMarkup()
        link_button.add(InlineKeyboardButton(
            text="Зв'язатися з кандидатом",
            url=f"https://t.me/{user_resume['username']}")
        )

        resume = (f"<b>Ім`я</b>\n{user_resume['name']}\n\n"
                  f"<b>Вік</b>\n{user_resume['age']}\n\n"
                  f"<b>Місто</b>\n{user_resume['city']}\n\n"
                  f"<b>Формат праці</b>\n{user_resume['workflow']}\n\n"
                  f"<b>Джерело праці</b>\n{user_resume['sources']}\n\n"
                  f"<b>Вертикаль</b>\n{user_resume['verticals']}\n\n"
                  f"<b>Гео</b>\n{user_resume['geo']}\n\n"
                  f"<b>Профіт</b>\n{user_resume['profit']}")

        if user_resume['statistic'] is not None:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=user_resume['statistic'],
                caption=resume,
                parse_mode=ParseMode.HTML,
                reply_markup=link_button
            )
        else:
            await call.message.answer(
                text=resume,
                parse_mode=ParseMode.HTML,
                reply_markup=link_button
            )

    else:
        await call.message.answer("Користувача вже не існує")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
