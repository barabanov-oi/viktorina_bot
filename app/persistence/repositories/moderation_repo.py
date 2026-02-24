from app.common.utils import utcnow
from app.persistence.models import ModerationFlag
from .base import BaseRepository


class ModerationRepository(BaseRepository):
    def resolve(self, flag_id: int, resolution: str) -> bool:
        flag = self.session.get(ModerationFlag, flag_id)
        if not flag:
            return False
        flag.status = resolution
        flag.resolved_at = utcnow()
        return True
