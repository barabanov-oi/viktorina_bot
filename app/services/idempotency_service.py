from app.persistence.unit_of_work import UnitOfWork


class IdempotencyService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def is_new(self, key: str, payload: dict, event_type: str = "idempotency") -> bool:
        with self.uow_factory() as uow:
            return uow.events.save_event(event_type=event_type, idempotency_key=key, payload=payload)
