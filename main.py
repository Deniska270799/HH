# main.py

from fastapi import FastAPI
from tasks1 import update_currency

app = FastAPI()


@app.get("/data", response_model=tuple | str)
async def get_data(total: int = 0):
    # Вызываем задачу update_currency
    result = update_currency.delay()
    # Ожидаем завершения задачи и получаем значение sp
    sp = result.get()
    # Возможно, вернуть текущий курс
    return f'Курс доллара = {sp["USD"]} рублей.\nКурс евро = {sp["EUR"]} рублей'


@app.post("/update_currency")
async def run_update_currency_task():
    # Вызываем задачу update_currency
    update_currency.delay()
    return {"message": "Задача обновления курса запущена"}

