import time

from app.common.logging import configure_logging
from app.config import get_settings
from app.persistence.unit_of_work import UnitOfWork
from app.services.leaderboard_service import LeaderboardService


class JobWorker:
    def __init__(self):
        self.running = True
        self.leaderboards = LeaderboardService()

    def process(self) -> None:
        with UnitOfWork() as uow:
            job = uow.jobs.pick_next()
            if not job:
                return
            try:
                if job.type == "recompute_leaderboards":
                    self.leaderboards.rebuild_global()
                job.status = "done"
                job.updated_at = job.created_at
            except Exception as exc:
                job.status = "failed"
                job.last_error = str(exc)
                job.attempts += 1


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    worker = JobWorker()
    while worker.running:
        worker.process()
        time.sleep(2)


if __name__ == "__main__":
    main()
