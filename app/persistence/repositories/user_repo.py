from sqlalchemy import select

from app.common.utils import utcnow
from app.persistence.models import User
from .base import BaseRepository


class UserRepository(BaseRepository):
    def get_or_create(self, tg_user_id: int, username: str | None, first_name: str | None) -> User:
        user = self.session.scalar(select(User).where(User.tg_user_id == tg_user_id))
        if user:
            return user
        user = User(
            tg_user_id=tg_user_id,
            username=username,
            first_name=first_name,
            created_at=utcnow(),
            is_banned=False,
            flags={},
        )
        self.session.add(user)
        self.session.flush()
        return user

    def ban(self, tg_user_id: int) -> bool:
        user = self.session.scalar(select(User).where(User.tg_user_id == tg_user_id))
        if not user:
            return False
        user.is_banned = True
        return True
