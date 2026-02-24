from app.domain.enums import Difficulty
from app.services.scoring import ScoringService


def test_scoring_correct_fast_answer_gives_bonus():
    svc = ScoringService()
    points = svc.score_answer(Difficulty.medium, True, 1200, streak=2)
    assert points > 20


def test_scoring_wrong_answer_is_zero():
    svc = ScoringService()
    assert svc.score_answer(Difficulty.hard, False, 500, streak=10) == 0
