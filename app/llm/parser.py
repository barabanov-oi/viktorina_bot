import json

from app.dto.question import GeneratedQuestionDTO


class LLMParseError(ValueError):
    pass


def parse_llm_question(raw: str) -> GeneratedQuestionDTO:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LLMParseError("LLM вернул невалидный JSON") from exc

    try:
        return GeneratedQuestionDTO.model_validate(payload)
    except Exception as exc:
        raise LLMParseError(f"Ошибка валидации LLM payload: {exc}") from exc
