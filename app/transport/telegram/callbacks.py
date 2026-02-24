from aiogram.filters.callback_data import CallbackData


class AnswerCb(CallbackData, prefix="ans"):
    session_id: int
    qi_id: int
    option: int
