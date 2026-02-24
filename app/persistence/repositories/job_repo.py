from sqlalchemy import select

from app.common.utils import utcnow
from app.persistence.models import Job
from .base import BaseRepository


class JobRepository(BaseRepository):
    def enqueue(self, type_: str, payload: dict) -> Job:
        job = Job(type=type_, payload=payload, status="queued", attempts=0, run_after=utcnow(), created_at=utcnow(), updated_at=utcnow())
        self.session.add(job)
        self.session.flush()
        return job

    def pick_next(self) -> Job | None:
        stmt = (
            select(Job)
            .where(Job.status == "queued", Job.run_after <= utcnow())
            .order_by(Job.id.asc())
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        job = self.session.scalar(stmt)
        if not job:
            return None
        job.status = "running"
        job.updated_at = utcnow()
        return job
