from models.models import CurrencyRates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import user, password, host, db, port

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_currency_rate(currency, rate):
    with SessionLocal() as session:
        new_rate = CurrencyRates(currency=currency, rate=rate)
        session.add(new_rate)
        session.commit()

