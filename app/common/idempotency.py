from dataclasses import dataclass


@dataclass(frozen=True)
class IdempotencyContext:
    source: str
    external_id: str

    @property
    def key(self) -> str:
        return f"{self.source}:{self.external_id}"
