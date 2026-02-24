from app.domain.enums import Difficulty
from app.services.anti_cheat import AntiCheatService
from app.services.scoring import ScoringService


class GameEngineService:
    def __init__(self):
        self.scoring = ScoringService()
        self.anti_cheat = AntiCheatService()

    def evaluate_answer(self, difficulty: Difficulty, is_correct: bool, answer_time_ms: int, streak: int) -> dict:
        anti = self.anti_cheat.evaluate(answer_time_ms)
        raw = self.scoring.score_answer(difficulty, is_correct, answer_time_ms, streak)
        points = int(raw * anti["multiplier"])
        return {"points": points, "anti_cheat": anti}
