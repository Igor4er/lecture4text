from aiogram.fsm.state import State, StatesGroup


class UpdateAPIKey(StatesGroup):
    deepgram = State()
    openai = State()
    gist = State()
