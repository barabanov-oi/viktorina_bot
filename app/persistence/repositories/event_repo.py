import random
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.common.utils import utcnow
from app.persistence.models import GameEvent
from .base import BaseRepository


class EventRepository(BaseRepository):
    def save_event(
        self,
        event_type: str,
        idempotency_key: str,
        payload: dict,
        session_id: int | None = None,
        user_id: int | None = None,
        chat_id: int | None = None,
    ) -> bool:
        event = GameEvent(
            id=random.randint(1, 2_000_000_000),
            session_id=session_id,
            user_id=user_id,
            chat_id=chat_id,
            event_type=event_type,
            payload=payload,
            created_at=utcnow(),
            idempotency_key=idempotency_key,
        )
        self.session.add(event)
        try:
            self.session.flush()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def exists_idempotency(self, key: str) -> bool:
        return self.session.scalar(select(GameEvent.id).where(GameEvent.idempotency_key == key)) is not None
