from fastapi import HTTPException, status, Response
import psycopg2
from datetime import datetime
import schemas, models, database

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_SERVER = os.getenv('POSTGRES_SERVER')
DB_NAME = os.getenv('POSTGRES_DB')

def open_connection():
    pgdb = psycopg2.connect(
      host=DB_SERVER,
      database=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD
    )
    return pgdb


#Helper function
def get_record_by_id(id, db):
    result = db.query(models.Record).filter(models.Record.id == id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No record found for id = {id}")
    return result

def validate_date(start_date, end_date):
    # try:
    #     str(date) == str(datetime.strptime(str(date), '%Y-%m-%d').date())
    # except ValueError:
    #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid date")
    if start_date > start_date.today():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid start date. Start date must be on or before today")
    if start_date > end_date:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid date range. Start date must be on or before end date")

def validate_country(country, db):
    result = db.query(models.Country).filter(models.Country.country == country).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Invalid country. Please refer to list of available country")
    return True


def fetch_query_results(query, placeholder):
    try:
        pgdb = open_connection()
    except psycopg2.Error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Could not connect to database")
    try:
        pgcursor = pgdb.cursor()
    except psycopg2.Error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database Error")
    try:
        pgcursor.execute(query, placeholder)
        pgresult = pgcursor.fetchall()
    except psycopg2.Error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Query to database failed!")
    pgcursor.close()
    return pgresult


# def modify_record(request, placeholder):
#     try:
#         pgdb = open_connection()
#     except psycopg2.Error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Could not connect to database")
#     try:
#         pgcursor = pgdb.cursor()
#     except psycopg2.Error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Database Error")
#     try:
#         pgcursor.execute(request, placeholder)
#         pgresult = pgcursor.fetchone()
#     except psycopg2.Error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Insert record into database failed!")
#     pgdb.commit()
#     pgcursor.close()
#     return pgresult


# def delete_record(request, placeholder):
#     try:
#         pgdb = open_connection()
#     except psycopg2.Error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Could not connect to database")
#     try:
#         pgcursor = pgdb.cursor()
#     except psycopg2.Error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Database Error")
#     try:
#         pgcursor.execute(request, placeholder)
#     except psycopg2.Error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Delete record from database failed!")
#     pgdb.commit()
#     pgcursor.close()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


def parse_to_summaryglobal(values):
    keys = schemas.get_summary_global_fields()
    return schemas.SummaryGlobal.parse_obj(dict(zip(keys, values)))

def parse_to_summarycountry(values):
    keys = schemas.get_summary_country_fields()
    return schemas.SummaryCountry.parse_obj(dict(zip(keys, values)))   
    
def parse_to_dailyglobal(values):
    keys = schemas.get_daily_global_fields()
    return schemas.DailyGlobal.parse_obj(dict(zip(keys, values)))

def parse_to_dailycountry(values):
    keys = schemas.get_daily_country_fields()
    return schemas.DailyCountry.parse_obj(dict(zip(keys, values)))     

def parse_to_record(values):
    keys = schemas.get_fields()
    return schemas.Record.parse_obj(dict(zip(keys, values)))  


def result_parser(pgresult, parse, detailmsg="No Record Found"):
    results = []
    if len(pgresult) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detailmsg)
    for result in pgresult:
        nextrecord = parse(result)
        results = results + [nextrecord]
    return results
