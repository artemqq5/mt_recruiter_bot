from aiogram.types import ReplyKeyboardRemove, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from buttons_.buttons_menu import cancel_state, set_menu_commands
from constants_.main_constants import ADD_RESUME_TEXT
from data_.repository import MyRepository
from states.resume_state import ResumeState


async def add_start_resume_cmd(message):
    await ResumeState.name.set()
    await message.answer("Як тебе звати?", reply_markup=cancel_state())


async def add_finish_resume_cmd(message, data):
    result = MyRepository().update_user(
        telegram_id=message.chat.id,
        name=data['name'],
        age=data['age'],
        city=data['city'],
        workflow=data['workflow'],
        sources=data['sources'],
        verticals=data['verticals'],
        geo=data['geo'],
        profit=data['profit'],
        statistic=data['statistic']
    )

    if result is not None:
        await message.answer(ADD_RESUME_TEXT, parse_mode=ParseMode.HTML, reply_markup=set_menu_commands(message))
    else:
        await message.answer(
            "Виникла помилка, не вдалося додати резюме, перезапустіть бот /start",
            reply_markup=ReplyKeyboardRemove()
        )


async def my_resume_cmd(bot, message):
    user = MyRepository().get_user(message.chat.id)
    if user is not None:
        if user['name'] is None:
            await message.answer(
                "У вас поки немає анкети, заповніть її зараз натиснувши на кнопку \n\n<b>Моя анкета</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=set_menu_commands(message)
            )
        else:
            resume = (f"<b>Ім`я</b>\n{user['name']}\n\n"
                      f"<b>Вік</b>\n{user['age']}\n\n"
                      f"<b>Місто</b>\n{user['city']}\n\n"
                      f"<b>Формат праці</b>\n{user['workflow']}\n\n"
                      f"<b>Джерело праці</b>\n{user['sources']}\n\n"
                      f"<b>Вертикаль</b>\n{user['verticals']}\n\n"
                      f"<b>Гео</b>\n{user['geo']}\n\n"
                      f"<b>Профіт</b>\n{user['profit']}")

            if user['statistic'] is not None:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=user['statistic'],
                    caption=resume,
                    parse_mode=ParseMode.HTML,
                    reply_markup=set_menu_commands(message)
                )
            else:
                await message.answer(text=resume, parse_mode=ParseMode.HTML, reply_markup=set_menu_commands(message))
    else:
        await message.answer("Виникла помилка, перезапустіть бот /start", reply_markup=ReplyKeyboardRemove())


async def all_resume_cmd(message):
    all_resume = MyRepository().all_users()
    if all_resume is not None:
        if len(all_resume) > 0:
            keyboard_markup = InlineKeyboardMarkup()
            for i in all_resume:
                if i['role'] == 'user':
                    resume = f"{i['name']} | {i['age']} | {i['city']}"
                    keyboard_markup.add(InlineKeyboardButton(resume, callback_data=f"resume_{i['telegram_id']}"))
                    await message.answer("Анкети користувачів:", reply_markup=keyboard_markup)
        else:
            await message.answer("Список поки пустий, чекайте на оновлення")
    else:
        await message.answer(
            "Помилка при отриманні даних, перезапустіть бот /start",
            reply_markup=ReplyKeyboardRemove()
        )
        print("error vacancies")
