from pydantic import BaseModel, Field


class BanUserRequest(BaseModel):
    tg_user_id: int
    reason: str = Field(default="manual")


class DeactivateQuestionRequest(BaseModel):
    question_id: int
    reason: str = Field(default="manual")


class ResolveModerationRequest(BaseModel):
    flag_id: int
    resolution: str = Field(default="resolved")
