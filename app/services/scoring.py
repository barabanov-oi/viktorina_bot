from app.domain.enums import Difficulty


class ScoringService:
    base_points = {
        Difficulty.easy: 10,
        Difficulty.medium: 20,
        Difficulty.hard: 35,
    }

    def score_answer(self, difficulty: Difficulty, is_correct: bool, answer_time_ms: int, streak: int) -> int:
        if not is_correct:
            return 0
        speed_bonus = max(0, 5000 - answer_time_ms) // 500
        streak_bonus = min(10, streak * 2)
        return self.base_points[difficulty] + speed_bonus + streak_bonus
