from typing import List

from pydantic import BaseModel


class Emotion(BaseModel):
    bbox: List[int]
    emotion: str
    confidence: float


class BaseResponse(BaseModel):
    message: str


class EmotionListResponse(BaseResponse):
    results: List[Emotion]
