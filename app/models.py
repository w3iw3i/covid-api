from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    province_state = Column(String(255), index=True)
    country_region = Column(String(255), nullable=False, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(Date, nullable=False, index=True)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    active = Column(Integer)
    new_confirmed = Column(Integer)
    new_deaths = Column(Integer)
    new_recovered = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Country(Base):
    __tablename__ = "country"

    country_id = Column(Integer, primary_key=True)
    country = Column(String(255), index=True)