FROM python:3.12-slim

WORKDIR /app

# Системные зависимости (psycopg2 любит иметь компилятор, но psycopg2-binary обычно хватает)
# Оставляем минимально
RUN pip install --no-cache-dir --upgrade pip

# Ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY . .

# Запуск
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
