from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, MetaData
from datetime import datetime

Base = declarative_base()
metadata = MetaData()
class CurrencyRates(Base):
    __tablename__ = 'currency_rates'
    id = Column(Integer, primary_key=True)
    currency = Column(String, nullable=False)
    rate = Column(Float)
    datetime = Column(TIMESTAMP, default=datetime.utcnow)
