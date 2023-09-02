import logging

from aiogram import Bot, Dispatcher, types, executor

from private import TELEGRAM_TOKEN_BOT

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN_BOT)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start_help(message: types.Message):
    if message.text == '/start':
        await message.answer("Привітальний текст")
    elif message.text == '/help':
        await message.answer("Інформація щодо бота")


@dp.message_handler(commands=['vacancies'])
async def start_help(message: types.Message):
    await message.answer("Буде відображено список актуальних вакансій")


@dp.message_handler()
async def echo(message: types.Message):
    # await message.answer(message.chat.us)
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
