from app.common.utils import stable_hash
from app.dto.question import GeneratedQuestionDTO
from app.llm.client import LLMClient
from app.llm.parser import parse_llm_question
from app.llm.prompt_builder import build_question_prompt
from app.persistence.models import Question
from app.persistence.unit_of_work import UnitOfWork


class QuestionService:
    def __init__(self, llm_client: LLMClient, uow_factory=UnitOfWork):
        self.llm_client = llm_client
        self.uow_factory = uow_factory

    def get_or_generate(self, topic_id: int, difficulty: str, language: str, session_id: int | None, user_id: int | None, chat_id: int | None) -> Question | None:
        with self.uow_factory() as uow:
            pool = uow.questions.list_topics_questions(topic_id, difficulty, language, limit=1)
            if pool:
                return pool[0]

        if self.llm_client.disabled:
            return None

        prompt_text = build_question_prompt(topic_id=topic_id, difficulty=difficulty, language=language)
        params = {"topic_id": topic_id, "difficulty": difficulty, "language": language}

        with self.uow_factory() as uow:
            log = uow.prompt_logs.create(
                user_id=user_id,
                chat_id=chat_id,
                session_id=session_id,
                prompt_version="v1",
                params=params,
                prompt_text=prompt_text,
                raw_response="",
                parsed_response=None,
                status="started",
                latency_ms=0,
            )
            response = self.llm_client.generate(prompt_text)
            dto: GeneratedQuestionDTO = parse_llm_question(response.raw)
            content_hash = stable_hash({"question": dto.question, "answers": dto.answers, "language": language})
            dup = uow.questions.get_by_hash(content_hash)
            if dup:
                log.status = "duplicate"
                log.raw_response = response.raw
                log.parsed_response = dto.model_dump()
                log.latency_ms = response.latency_ms
                return dup
            question = Question(
                topic_id=topic_id,
                language=language,
                difficulty=difficulty,
                text=dto.question,
                options=dto.answers,
                correct_index=dto.correct_index,
                explanation=dto.explanation,
                tags=dto.tags,
                source="llm",
                content_hash=content_hash,
                created_at=response.created_at,
                is_active=True,
            )
            uow.session.add(question)
            log.status = "ok"
            log.raw_response = response.raw
            log.parsed_response = dto.model_dump()
            log.latency_ms = response.latency_ms
            return question
