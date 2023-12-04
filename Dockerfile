FROM python:3.10

RUN pip install fastapi uvicorn psycopg2 requests beautifulsoup4


COPY psql.py /app/
COPY main.py /app/

WORKDIR /app

# Запускаем FastAPI-приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

