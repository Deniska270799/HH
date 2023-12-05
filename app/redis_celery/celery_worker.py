from celery import Celery
from config import redis_host, redis_port, redis_db, api_key
import json
from app.db.psql import save_currency_rate
import requests
import redis


redis_instance = redis.StrictRedis(host=redis_host, port=int(redis_port), db=int(redis_db))
# Настройка Celery для использования Redis
celery_app = Celery("currency_worker", broker=f"redis://{redis_host}:{redis_port}/{redis_db}")
# Список валют
key_currencies = ('RUB', 'EUR', 'BTC', 'CNY', 'USD')


@celery_app.task
def fetch_currency_data():
    try:
        headers = {'apikey': api_key}
        response = requests.get('https://api.currencyapi.com/v3/latest', headers=headers)
        response.raise_for_status()  # Бросит исключение, если ответ не успешный (не 200-299)
        data = response.json()

        exchange_rates = {}
        for currency in key_currencies:
            rate = data['data'][currency]['value']
            save_currency_rate(currency, rate)
            exchange_rates[currency] = rate

        redis_instance.setex("currency_data", 600, json.dumps(exchange_rates)) # 10 минут в секундах

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except KeyError as e:
        print(f"Ошибка в данных ответа API: {e}")


# Настройка расписания для Celery
celery_app.conf.beat_schedule = {
    "fetch-currency-data-every-15-minutes": {
        "task": "app.redis_celery.celery_worker.fetch_currency_data",
        "schedule": 900.0,  # 15 минут в секундах
    }
}
