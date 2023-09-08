from aiogram.dispatcher.filters.state import StatesGroup, State


class AddVacancyState(StatesGroup):
    title = State()
    requirements = State()
    responsibilities = State()
    bonus = State()
    contact = State()
