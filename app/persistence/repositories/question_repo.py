from sqlalchemy import select

from app.persistence.models import Question
from .base import BaseRepository


class QuestionRepository(BaseRepository):
    def list_topics_questions(self, topic_id: int, difficulty: str, language: str, limit: int) -> list[Question]:
        stmt = (
            select(Question)
            .where(
                Question.topic_id == topic_id,
                Question.difficulty == difficulty,
                Question.language == language,
                Question.is_active.is_(True),
            )
            .limit(limit)
        )
        return list(self.session.scalars(stmt))

    def get_by_hash(self, content_hash: str) -> Question | None:
        return self.session.scalar(select(Question).where(Question.content_hash == content_hash))

    def deactivate(self, question_id: int) -> bool:
        q = self.session.get(Question, question_id)
        if not q:
            return False
        q.is_active = False
        return True
