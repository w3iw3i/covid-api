from fastapi import APIRouter, HTTPException, Response, status, Depends
from typing import List
from datetime import date, datetime, timedelta
import schemas, models, database, helper
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = '/summary',
    tags = ['Summary']
)


# Get global summary records
@router.get("/global", response_model=List[schemas.SummaryGlobal], status_code=status.HTTP_200_OK)
async def get_global_summary_records(start_date: date = date.today() - timedelta(1), end_date: date = date.today()):
    helper.validate_date(start_date, end_date)
    query = "SELECT date, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active), MAX(updated_at) from records WHERE date BETWEEN %s AND %s GROUP BY date"
    placeholder = (start_date, end_date)
    myresult = helper.fetch_query_results(query, placeholder)
    results = helper.result_parser(myresult, helper.parse_to_summaryglobal)
    return results


# Get summary records by country
@router.get("/country", response_model=List[schemas.SummaryCountry], status_code=status.HTTP_200_OK)
async def get_country_summary_records(country: str = 'Singapore', start_date: date = date.today() - timedelta(1), end_date: date = date.today(), db: Session = Depends(database.get_db)):
    country = country.lower().capitalize()
    helper.validate_country(country, db)
    helper.validate_date(start_date, end_date)
    query = "SELECT date, country_region, latitude, longitude, confirmed, deaths, recovered, active, updated_at from records WHERE country_region = %s AND date BETWEEN %s AND %s"
    placeholder = (country, start_date, end_date)
    myresult = helper.fetch_query_results(query, placeholder)
    results = helper.result_parser(myresult, helper.parse_to_summarycountry)
    return results


# Get summary record by id
@router.get("/{id}", response_model=schemas.Record, status_code=status.HTTP_200_OK)
async def get_record(id: int, db: Session = Depends(database.get_db)):
    return helper.get_record_by_id(id, db)


# Insert record into data table
@router.post("/", response_model=schemas.Record, status_code=status.HTTP_201_CREATED)
async def add_record(request: schemas.RecordRequest, db: Session = Depends(database.get_db)):
    # query = "INSERT INTO records (province_state, country_region, latitude, longitude, date, confirmed, deaths, recovered, active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # placeholder = (province_state, country_region, latitude, longitude, date, confirmed, deaths, recovered, active)
    # myresult = helper.modify_record(query, placeholder)
    # results = helper.result_parser(myresult, helper.parse_to_record)
    record = models.Record(
        country_region = request.country_region,
        province_state = request.province_state,
        date = request.date,
        latitude = request.latitude,
        longitude = request.longitude,
        confirmed = request.confirmed,
        deaths = request.deaths,
        recovered = request.recovered,
        active = request.active
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# Delete record by id
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_record(id: int, db: Session = Depends(database.get_db)):
    # query = "DELETE from records WHERE id = %s"
    # placeholder = (id,)
    # helper.delete_record(query, placeholder)
    result = helper.get_record_by_id(id, db)
    db.delete(result)
    db.commit()
    return Response(status_code=status.HTTP_200_OK, headers={"message": "Record has been successfully deleted"})


# Update record by id
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_record(id: int, request: schemas.RecordRequest, db: Session = Depends(database.get_db)):
    result = db.query(models.Record).filter(models.Record.id == id)
    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No record found for id = {id}")
    result.update({
        models.Record.province_state : request.province_state,
        models.Record.country_region : request.country_region,
        models.Record.date : request.date,
        models.Record.latitude : request.latitude,
        models.Record.longitude : request.longitude,
        models.Record.confirmed : request.confirmed,
        models.Record.deaths : request.deaths,
        models.Record.recovered : request.recovered,
        models.Record.active : request.active
    })
    db.commit()
    return Response(status_code=status.HTTP_200_OK, headers={"message": "Record has been successfully updated"})






