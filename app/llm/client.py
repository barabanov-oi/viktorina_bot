import time
from dataclasses import dataclass

from app.common.utils import utcnow
from app.config import get_settings


@dataclass
class LLMResponse:
    raw: str
    latency_ms: int
    created_at: object


class LLMClient:
    def __init__(self):
        settings = get_settings()
        self.disabled = settings.llm_disabled or not settings.llm_api_key

    def generate(self, prompt: str) -> LLMResponse:
        start = time.time()
        # MVP provider-agnostic mock transport; можно подменить HTTP-клиентом.
        raw = '{"question":"Столица Франции?","answers":["Берлин","Париж","Рим","Мадрид"],"correct_index":1,"explanation":"Париж — столица Франции.","tags":["география","европа"]}'
        latency_ms = int((time.time() - start) * 1000)
        return LLMResponse(raw=raw, latency_ms=latency_ms, created_at=utcnow())
