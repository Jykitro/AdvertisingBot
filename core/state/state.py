from aiogram.fsm.state import State, StatesGroup


class QuestionState(StatesGroup):
    age = State()
    how_did_you_hear_about_us = State()
    financial_goal = State()
    take_time = State()
    partnership_participation = State()
    your_nationality = State()
    name = State()
    phone_number = State()
    confirm = State()
