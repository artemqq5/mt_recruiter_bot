from aiogram.dispatcher.filters.state import StatesGroup, State


class VacancyState(StatesGroup):
    title = State()
    requirements = State()
    responsibilities = State()
    bonus = State()
    contact = State()
