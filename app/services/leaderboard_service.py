from app.persistence.unit_of_work import UnitOfWork


class LeaderboardService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def rebuild_global(self) -> None:
        with self.uow_factory() as uow:
            uow.leaderboards.rebuild_scope("global", None)

    def top_global(self, limit: int = 10):
        with self.uow_factory() as uow:
            return uow.leaderboards.top("global", None, limit)
