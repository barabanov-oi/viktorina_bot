from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.common.utils import utcnow
from app.persistence.db import Base
from app.persistence.models import GameEvent
from app.persistence.repositories.event_repo import EventRepository


def test_event_idempotency_unique():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        repo = EventRepository(session)
        ok1 = repo.save_event("x", "k1", {"a": 1})
        session.commit()
        ok2 = repo.save_event("x", "k1", {"a": 1})
        assert ok1 is True
        assert ok2 is False
        assert session.query(GameEvent).count() == 1
