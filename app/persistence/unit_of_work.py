from app.persistence.db import SessionLocal
from app.persistence.repositories.event_repo import EventRepository
from app.persistence.repositories.job_repo import JobRepository
from app.persistence.repositories.leaderboard_repo import LeaderboardRepository
from app.persistence.repositories.moderation_repo import ModerationRepository
from app.persistence.repositories.prompt_log_repo import PromptLogRepository
from app.persistence.repositories.question_repo import QuestionRepository
from app.persistence.repositories.user_repo import UserRepository


class UnitOfWork:
    def __enter__(self):
        self.session = SessionLocal()
        self.users = UserRepository(self.session)
        self.questions = QuestionRepository(self.session)
        self.events = EventRepository(self.session)
        self.leaderboards = LeaderboardRepository(self.session)
        self.prompt_logs = PromptLogRepository(self.session)
        self.moderation = ModerationRepository(self.session)
        self.jobs = JobRepository(self.session)
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
