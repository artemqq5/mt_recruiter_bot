from aiogram.dispatcher.filters.state import StatesGroup, State


class ResumeState(StatesGroup):
    name = State()
    age = State()
    city = State()
    workflow = State()
    sources = State()
    verticals = State()
    geo = State()
    profit = State()
    statistic = State()
