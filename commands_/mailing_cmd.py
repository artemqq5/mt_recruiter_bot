from aiogram.types import ReplyKeyboardRemove

from buttons_.buttons_menu import set_menu_commands, cancel_state
from data_.repository import MyRepository
from states.mailing_state import MailingState


async def mailing_message_cmd(message):
    await MailingState.mailing.set()
    await message.answer("Введіть повідомлення для всіх кандидатів:", reply_markup=cancel_state())


async def mailing_user_cmd(bot, message):
    users = MyRepository().all_candidates()
    unsuccessful = 1
    user_error = ""

    if users is not None:
        for i in users:
            try:
                if i['telegram_id'] != str(message.chat.id):
                    await bot.send_message(i['telegram_id'], message.text)
            except Exception as e:
                print(f"mailing all error for user {i}: {e}")
                unsuccessful += 1
                user_error += f"{i['username']}\n"

        await message.answer(
            text=f"📬 Успішно доставлено {len(users) - unsuccessful} користувачам з {len(users)}\n\n"
                 f"Досі не зареєструвалися у боті: \n{user_error}",
            reply_markup=set_menu_commands(message)
        )
    else:
        await message.answer(
            "Помилка при отриманні даних, перезапустіть бот /start",
            reply_markup=ReplyKeyboardRemove()
        )
