from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Создаём приложение FastAPI
app = FastAPI(title="Dowell API", version="0.1.0")

# CORS нужен, чтобы фронтенд (другой порт) мог делать запросы к API
# На этапе разработки разрешаем всё (потом можно ужесточить)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """
    Простой эндпоинт проверки: если он отвечает,
    значит сервер запущен и работает.
    """
    return {"status": "ok", "service": "dowell-backend"}
