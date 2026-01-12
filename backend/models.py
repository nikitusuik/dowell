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


from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import relationship


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Date, nullable=False, unique=True)  # один лог на дату
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    failed = Column(Boolean, nullable=False, default=False)
    score = Column(Integer, nullable=False, default=0)

    completed_count = Column(Integer, nullable=False, default=0)
    total_count = Column(Integer, nullable=False, default=0)

    items = relationship("DailyLogItem", back_populates="log", cascade="all, delete-orphan")


class DailyLogItem(Base):
    __tablename__ = "daily_log_items"

    id = Column(Integer, primary_key=True, index=True)

    log_id = Column(Integer, ForeignKey("daily_logs.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)

    value = Column(Float, nullable=True)
    passed = Column(Boolean, nullable=False, default=False)
    quality = Column(Float, nullable=False, default=0.0)

    log = relationship("DailyLog", back_populates="items")
