import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Берём строку подключения из переменной окружения (её зададим в docker-compose)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dowell:dowell@localhost:5432/dowell")

# Создаём engine (пул соединений)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


# Dependency для FastAPI: на каждый запрос создаём сессию и закрываем
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
