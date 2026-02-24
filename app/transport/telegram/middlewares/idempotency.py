from aiogram import BaseMiddleware

from app.services.idempotency_service import IdempotencyService


class IdempotencyMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.service = IdempotencyService()

    async def __call__(self, handler, event, data):
        update = data.get("event_update")
        update_id = getattr(update, "update_id", None)
        if update_id is None:
            return await handler(event, data)
        key = f"telegram_update:{update_id}"
        if not self.service.is_new(key=key, payload={"type": "update"}, event_type="telegram_update"):
            return None
        return await handler(event, data)
