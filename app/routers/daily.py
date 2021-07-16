from fastapi import APIRouter, HTTPException, Response, status, Depends
from typing import List
from datetime import date, datetime, timedelta
import schemas, models, database, helper
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = '/daily',
    tags = ['Daily']
)

# Get global daily new records
@router.get("/global", response_model=List[schemas.DailyGlobal], status_code=status.HTTP_200_OK)
async def get_global_daily_new_records(start_date: date = date.today() - timedelta(1), end_date: date = date.today()):
    helper.validate_date(start_date, end_date)
    query = "SELECT date, SUM(new_confirmed), SUM(new_deaths), SUM(new_recovered), MAX(updated_at) from records WHERE date BETWEEN %s AND %s GROUP BY date"
    placeholder = (start_date, end_date)
    myresult = helper.fetch_query_results(query, placeholder)
    results = helper.result_parser(myresult, helper.parse_to_dailyglobal)
    return results


# Get daily new records by country
@router.get("/country", response_model=List[schemas.DailyCountry], status_code=status.HTTP_200_OK)
async def get_country_daily_new_records(country: str = 'Singapore', start_date: date = date.today() - timedelta(1), end_date: date = date.today(), db: Session = Depends(database.get_db)):
    country = country.lower().capitalize()
    helper.validate_country(country, db)
    helper.validate_date(start_date, end_date)
    query = "SELECT date, country_region, latitude, longitude, new_confirmed, new_deaths, new_recovered, updated_at from records WHERE country_region = %s AND date BETWEEN %s AND %s"
    placeholder = (country, start_date, end_date)
    myresult = helper.fetch_query_results(query, placeholder)
    results = helper.result_parser(myresult, helper.parse_to_dailycountry)
    return results