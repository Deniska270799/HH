from fastapi import APIRouter, HTTPException, Depends
from app.schemas.schemas_for_users import CurrencyRatesResponse, Currency_Convert
from app.db.psql import SessionLocal
from app.dependencies import get_redis_instance
import json
import redis
from sqlalchemy import text

router = APIRouter()

@router.get("/data", response_model=CurrencyRatesResponse)
async def get_data(redis_instance: redis.StrictRedis = Depends(get_redis_instance)):
    currency_data = redis_instance.get("currency_data")
    if currency_data:
        return CurrencyRatesResponse(rates=currency_data)
    else:
        raise HTTPException(status_code=404, detail="Данные о валютах не найдены")

@router.post("/convert")
async def convert_currency(request: Currency_Convert, redis_instance: redis.StrictRedis = Depends(get_redis_instance)):
    currency_data = redis_instance.get("currency_data")
    if not currency_data:
        with SessionLocal() as session:
            # Сырой SQL-запрос для получения последних курсов валют
            sql_query = text("""
                        SELECT DISTINCT ON (currency) currency, rate
                        FROM currency_rates
                        ORDER BY currency, datetime DESC
                    """)
            result = session.execute(sql_query)
            exchange_rates = {row.currency: row.rate for row in result}
    else:
        exchange_rates = json.loads(currency_data)

    if request.currency not in exchange_rates:
        raise HTTPException(status_code=404, detail=f"Курс для валюты {request.currency} не найден")

    converted_values = {}
    amount_in_usd = request.amount / exchange_rates[request.currency] if request.currency != "USD" else request.amount
    for other_currency in exchange_rates:
        if other_currency != request.currency:
            converted_amount = amount_in_usd * exchange_rates[other_currency]
            converted_values[other_currency] = converted_amount

    return {
        "your_currency": request.currency,
        "your_amount": request.amount,
        "converted_currencies": converted_values
    }
