Запуск main: (FastAPI + Redis)
	uvicorn app.main:app --reload
Запуск celery_worker: (Redis + Celery)
	celery -A app.redis_celery.celery_worker.celery_app worker --loglevel=info --beat



