from sqlalchemy import create_engine, Column, Float, Integer, MetaData, Table, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:527619@localhost/Test"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()

# Определяем таблицу currency_rates с колонками usd_rate и eur_rate
currency_rates = Table(
    "currency_rates",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("usd_rate", Float),
    Column("eur_rate", Float),
)

class CurrencyRates(Base):
    __table__ = currency_rates

Base.metadata.create_all(bind=engine)

def save_currency_rates(usd_rate, eur_rate):
    with SessionLocal() as session:
        db_currency_rates = CurrencyRates(usd_rate=usd_rate, eur_rate=eur_rate)
        session.add(db_currency_rates)
        session.commit()
