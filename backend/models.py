from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, func
from db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=True)

    unit = Column(String(50), nullable=False, default="reps")  # reps/pages/glasses/minutes/km/custom
    min_value = Column(Float, nullable=False, default=1)
    target_value = Column(Float, nullable=False, default=1)

    weight = Column(Float, nullable=False, default=1.0)

    active = Column(Boolean, nullable=False, default=True)
    important = Column(Boolean, nullable=False, default=False)

    category = Column(String(50), nullable=False, default="custom")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
