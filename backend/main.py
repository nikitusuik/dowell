from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskOut

from datetime import date
from log_schemas import SubmitDayPayload, DailyLogOut, DailyLogItemOut
from models import DailyLog, DailyLogItem


app = FastAPI(title="Dowell API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проде ограничим
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "dowell-backend"}

# ---- CRUD Tasks ----

@app.get("/api/tasks", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id.asc()).all()

@app.get("/api/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    # Доп. логика: цель должна быть >= минимуму (по твоим правилам)
    if payload.target_value < payload.min_value:
        raise HTTPException(status_code=400, detail="target_value must be >= min_value")

    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.put("/api/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = payload.model_dump(exclude_unset=True)

    # Если обновляются min/target — проверим правило target >= min
    new_min = data.get("min_value", task.min_value)
    new_target = data.get("target_value", task.target_value)
    if new_target < new_min:
        raise HTTPException(status_code=400, detail="target_value must be >= min_value")

    for key, value in data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return None

@app.post("/api/logs/today/submit", response_model=DailyLogOut)
def submit_today(payload: SubmitDayPayload, db: Session = Depends(get_db)):
    # 1) берём сегодняшнюю дату на сервере
    today = date.today()

    # 2) подтягиваем активные задачи
    tasks = db.query(Task).filter(Task.active == True).all()
    task_map = {t.id: t for t in tasks}

    # 3) превращаем payload в {task_id: value}
    values = {i.task_id: i.value for i in payload.items}

    rows = []
    for t in tasks:
        raw = values.get(t.id, None)
        safe = float(raw) if raw is not None else 0.0

        passed = safe >= float(t.min_value)
        quality = min(safe / float(t.target_value), 1.0) if float(t.target_value) > 0 else 0.0

        rows.append((t, raw, passed, quality))

    total_count = len(rows)
    completed_count = sum(1 for (_, _, passed, _) in rows if passed)
    failed_count = sum(1 for (_, _, passed, _) in rows if not passed)
    failed = failed_count > 1

    sum_weight = sum(float(t.weight or 1.0) for (t, _, _, _) in rows) or 1.0
    weighted_quality = sum(float(t.weight or 1.0) * q for (t, _, _, q) in rows)
    score = int((weighted_quality / sum_weight) * 100)
    if failed:
        score = 0

    # 4) если на сегодня уже есть лог — перезаписываем (удалим старый)
    existing = db.query(DailyLog).filter(DailyLog.day == today).first()
    if existing:
        db.delete(existing)
        db.commit()

    log = DailyLog(
        day=today,
        failed=failed,
        score=score,
        completed_count=completed_count,
        total_count=total_count,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    items_out = []
    for (t, raw, passed, quality) in rows:
        item = DailyLogItem(
            log_id=log.id,
            task_id=t.id,
            value=float(raw) if raw is not None else None,
            passed=passed,
            quality=float(quality),
        )
        db.add(item)

        items_out.append(DailyLogItemOut(
            task_id=t.id,
            value=float(raw) if raw is not None else None,
            passed=passed,
            quality=float(quality),
        ))

    db.commit()

    return DailyLogOut(
        day=today,
        failed=failed,
        score=score,
        completed_count=completed_count,
        total_count=total_count,
        items=items_out,
    )


@app.get("/api/logs/month")
def get_month(db: Session = Depends(get_db)):
    # Отдаём список дней (самое нужное для страницы /month)
    logs = db.query(DailyLog).order_by(DailyLog.day.desc()).all()
    return [
        {
            "day": str(l.day),
            "score": l.score,
            "failed": l.failed,
            "completed_count": l.completed_count,
            "total_count": l.total_count,
        }
        for l in logs
    ]
