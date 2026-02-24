from sqlalchemy import delete, func, select

from app.common.utils import utcnow
from app.persistence.models import LeaderboardCache, RatingEvent
from .base import BaseRepository


class LeaderboardRepository(BaseRepository):
    def rebuild_scope(self, scope: str, scope_id: str | None = None) -> None:
        self.session.execute(delete(LeaderboardCache).where(LeaderboardCache.scope == scope, LeaderboardCache.scope_id == scope_id))
        stmt = select(RatingEvent.user_id, func.sum(RatingEvent.delta_points).label("points")).group_by(RatingEvent.user_id)
        if scope == "chat" and scope_id:
            stmt = stmt.where(RatingEvent.chat_id == int(scope_id))
        rows = list(self.session.execute(stmt))
        rows.sort(key=lambda x: x.points, reverse=True)
        for idx, row in enumerate(rows, start=1):
            self.session.add(
                LeaderboardCache(
                    scope=scope,
                    scope_id=scope_id,
                    user_id=row.user_id,
                    points=int(row.points or 0),
                    rank=idx,
                    updated_at=utcnow(),
                )
            )

    def top(self, scope: str, scope_id: str | None, limit: int) -> list[LeaderboardCache]:
        stmt = (
            select(LeaderboardCache)
            .where(LeaderboardCache.scope == scope, LeaderboardCache.scope_id == scope_id)
            .order_by(LeaderboardCache.rank.asc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt))
