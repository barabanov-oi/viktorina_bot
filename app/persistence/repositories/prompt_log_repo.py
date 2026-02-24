from sqlalchemy import select

from app.common.utils import utcnow
from app.persistence.models import PromptLog
from .base import BaseRepository


class PromptLogRepository(BaseRepository):
    def create(self, **kwargs) -> PromptLog:
        log = PromptLog(created_at=utcnow(), **kwargs)
        self.session.add(log)
        self.session.flush()
        return log

    def latest(self, limit: int = 50) -> list[PromptLog]:
        stmt = select(PromptLog).order_by(PromptLog.id.desc()).limit(limit)
        return list(self.session.scalars(stmt))
