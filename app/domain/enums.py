from enum import Enum


class GameMode(str, Enum):
    solo = "solo"
    group = "group"
    duel = "duel"
    tournament = "tournament"


class SessionStatus(str, Enum):
    active = "active"
    finished = "finished"
    cancelled = "cancelled"


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class QuestionSource(str, Enum):
    bank = "bank"
    llm = "llm"
