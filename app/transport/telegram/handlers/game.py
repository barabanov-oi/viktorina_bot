from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("quiz"))
async def quiz_cmd(message: Message) -> None:
    await message.answer("MVP: solo-сессия создана. В следующей версии здесь будет полноценный game loop.")


@router.message(Command("topics"))
async def topics_cmd(message: Message) -> None:
    await message.answer("Темы: history, science, movies, sport")


@router.message(Command("groupquiz"))
async def groupquiz_cmd(message: Message) -> None:
    await message.answer("Групповой режим: окно вступления 30 секунд. Используйте /join")


@router.message(Command("join"))
async def join_cmd(message: Message) -> None:
    await message.answer("Вы присоединились к групповой игре (MVP).")


@router.message(Command("duel"))
async def duel_cmd(message: Message) -> None:
    await message.answer("Duel MVP: приглашение отправлено.")


@router.message(Command("duel_random"))
async def duel_random_cmd(message: Message) -> None:
    await message.answer("Duel random MVP: ищу соперника...")


@router.message(Command("rank"))
async def rank_cmd(message: Message) -> None:
    await message.answer("Ваш рейтинг: в разработке (используйте /top)")


@router.message(Command("top"))
async def top_cmd(message: Message) -> None:
    await message.answer("Топ игроков: MVP")


@router.message(Command("report"))
async def report_cmd(message: Message) -> None:
    await message.answer("Жалоба принята на модерацию.")


@router.message(Command("admin_help"))
async def admin_help_cmd(message: Message) -> None:
    await message.answer("Admin: используйте веб API /admin/* с токеном.")
