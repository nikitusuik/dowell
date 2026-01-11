from datetime import datetime
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)

    unit: str = Field(..., min_length=1, max_length=50)  # reps/pages/glasses/minutes/km/custom
    min_value: float = Field(..., gt=0)
    target_value: float = Field(..., gt=0)

    weight: float = Field(default=1.0, gt=0)

    active: bool = True
    important: bool = False
    category: str = Field(default="custom", min_length=1, max_length=50)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    # В update разрешим частичное обновление (PATCH мы не используем, но PUT тоже можно так делать)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)

    unit: str | None = Field(default=None, min_length=1, max_length=50)
    min_value: float | None = Field(default=None, gt=0)
    target_value: float | None = Field(default=None, gt=0)

    weight: float | None = Field(default=None, gt=0)
    active: bool | None = None
    important: bool | None = None
    category: str | None = Field(default=None, min_length=1, max_length=50)

class TaskOut(TaskBase):
    id: int
    created_at: datetime | None = None
