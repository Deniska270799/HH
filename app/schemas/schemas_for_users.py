import json
from pydantic import BaseModel, validator
from typing import Dict

class CurrencyRatesResponse(BaseModel):
    rates: Dict[str, float]

    @validator('rates', pre=True)
    def parse_rates(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

class Currency_Convert(BaseModel):
    currency: str
    amount: float