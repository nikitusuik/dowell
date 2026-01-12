from datetime import date
from pydantic import BaseModel, Field

class SubmitItem(BaseModel):
    task_id: int
    value: float | None = None

class SubmitDayPayload(BaseModel):
    items: list[SubmitItem] = Field(default_factory=list)

class DailyLogItemOut(BaseModel):
    task_id: int
    value: float | None
    passed: bool
    quality: float

class DailyLogOut(BaseModel):
    day: date
    failed: bool
    score: int
    completed_count: int
    total_count: int
    items: list[DailyLogItemOut]
