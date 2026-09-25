from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
    )

    conversation_id: str | None = None


class ChatResponse(BaseModel):
    message: str

    conversation_id: str

    intent: str | None = None

    intent_confidence: float | None = None