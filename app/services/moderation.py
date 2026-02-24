from app.persistence.unit_of_work import UnitOfWork


class ModerationService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def ban_user(self, tg_user_id: int) -> bool:
        with self.uow_factory() as uow:
            return uow.users.ban(tg_user_id)

    def deactivate_question(self, question_id: int) -> bool:
        with self.uow_factory() as uow:
            return uow.questions.deactivate(question_id)

    def resolve_flag(self, flag_id: int, resolution: str) -> bool:
        with self.uow_factory() as uow:
            return uow.moderation.resolve(flag_id, resolution)
