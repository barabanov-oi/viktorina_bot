from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message) -> None:
    await message.answer("Привет! Я бот викторин. Команды: /help /quiz /top /rank")


@router.message(Command("help"))
async def help_cmd(message: Message) -> None:
    await message.answer(
        "Доступные команды:\n"
        "/quiz - начать solo\n/topics - список тем\n/groupquiz - групповая викторина\n/join - вступить\n"
        "/duel @user - дуэль\n/duel_random - случайная дуэль\n/rank - ваш рейтинг\n/top - топ"
    )
