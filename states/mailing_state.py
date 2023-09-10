from aiogram.dispatcher.filters.state import StatesGroup, State


class MailingState(StatesGroup):
    mailing = State()
