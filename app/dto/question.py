from pydantic import BaseModel, Field, field_validator


class GeneratedQuestionDTO(BaseModel):
    question: str = Field(min_length=10, max_length=1000)
    answers: list[str] = Field(min_length=4, max_length=4)
    correct_index: int
    explanation: str = Field(min_length=3, max_length=1000)
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("correct_index")
    @classmethod
    def validate_correct_index(cls, value: int) -> int:
        if value < 0 or value > 3:
            raise ValueError("correct_index должен быть в диапазоне 0..3")
        return value

    @field_validator("answers")
    @classmethod
    def validate_answers_unique(cls, value: list[str]) -> list[str]:
        if len({x.strip().lower() for x in value}) != 4:
            raise ValueError("answers должны содержать 4 уникальных варианта")
        return value
