from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class Record(BaseModel):
    id: int
    province_state: Optional[str] = None
    country_region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    date: date
    confirmed: Optional[int] = None
    deaths: Optional[int] = None
    recovered: Optional[int] = None
    active: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config():
        orm_mode = True


def get_fields():
    return ["id", "province_state", "country_region", "latitude", "longitude",
            "date", "confirmed", "deaths", "recovered", "active", 
            "created_at", "updated_at"]


class RecordRequest(BaseModel):
    province_state: Optional[str] = None
    country_region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    date: date
    confirmed: Optional[int] = None
    deaths: Optional[int] = None
    recovered: Optional[int] = None
    active: Optional[int] = None

    class Config():
        orm_mode = True


class SummaryGlobal(BaseModel):
    date: date
    total_confirmed: Optional[int] = None
    total_deaths: Optional[int] = None
    total_recovered: Optional[int] = None
    total_active: Optional[int] = None
    last_updated: datetime
    
    class Config():
        orm_mode = True

def get_summary_global_fields():
    return ["date", "total_confirmed", "total_deaths", "total_recovered", "total_active", "last_updated"]


class SummaryCountry(BaseModel):
    date: date
    country_region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    total_confirmed: Optional[int] = None
    total_deaths: Optional[int] = None
    total_recovered: Optional[int] = None
    total_active: Optional[int] = None
    last_updated: datetime
    
    class Config():
        orm_mode = True

def get_summary_country_fields():
    return ["date", "country_region", "latitude", "longitude", "total_confirmed", "total_deaths", "total_recovered", "total_active", "last_updated"]


class DailyGlobal(BaseModel):
    date: date
    new_confirmed: Optional[int] = None
    new_deaths: Optional[int] = None
    new_recovered: Optional[int] = None
    last_updated: datetime
    
    class Config():
        orm_mode = True

def get_daily_global_fields():
    return ["date", "new_confirmed", "new_deaths", "new_recovered", "last_updated"]


class DailyCountry(BaseModel):
    date: date
    country_region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    new_confirmed: Optional[int] = None
    new_deaths: Optional[int] = None
    new_recovered: Optional[int] = None
    last_updated: datetime
    
    class Config():
        orm_mode = True

def get_daily_country_fields():
    return ["date", "country_region", "latitude", "longitude", "new_confirmed", "new_deaths", "new_recovered", "last_updated"]