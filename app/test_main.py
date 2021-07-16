from fastapi import status
from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)

id_1 = 1
id_2 = 2
id_3 = 3

status200 = status.HTTP_200_OK
status201 = status.HTTP_201_CREATED
status400 = status.HTTP_400_BAD_REQUEST
status404 = status.HTTP_404_NOT_FOUND
status422 = status.HTTP_422_UNPROCESSABLE_ENTITY


# Sample data for testing
data = [
    {
    "province_state": None,
    "country_region": "Singapore",
    "latitude": None,
    "longitude": None,
    "date": "2021-07-10",
    "confirmed": 1,
    "deaths": 1,
    "recovered": 1,
    "active": 1
    },
    {
    "province_state": "Johor",
    "country_region": "Malaysia",
    "latitude": 123.45,
    "longitude": 543.21,
    "date": "2021-07-11",
    "confirmed": 1,
    "deaths": 1,
    "recovered": 1,
    "active": 1,
    },
    {
    "province_state": "Bangkok",
    "country_region": "Thailand",
    "latitude": None,
    "longitude": None,
    "date": "2021-07-12",
    "confirmed": None,
    "deaths": 1,
    "recovered": 1,
    "active": 1
    },
    {
    "province_state": "None",
    "country_region": "Singapore",
    "latitude": "def",
    "longitude": 12,
    "date": "2021-07-12",
    "confirmed": "abc",
    "deaths": 1,
    "recovered": 1,
    "active": 1
    }]


# Test root endpoint
def test_read_main():
    response = client.get("/")
    assert response.status_code == status200
    assert response.json() == {"message": "Welcome to Covid API Landing Page!"}

# Test get record
@pytest.mark.parametrize("url,status_code", [
                        (f"/summary/{id_1}", status200), 
                        (f"/summary/-1", status404)
                        ])
def test_get_record(url, status_code):
    response = client.get(url)
    assert response.status_code == status_code

# Test create record
@pytest.mark.parametrize("url,data,status_code", [
                        ("/summary/", data[0], status201), 
                        ("/summary/", data[1], status201), 
                        ("/summary/", data[2], status201),
                        ("/summary/", data[3], status422)
                        ])
def test_add_record(url, data, status_code):
    response = client.post(url, json=data)
    assert response.status_code == status_code

# Test update record
@pytest.mark.parametrize("url,data,status_code", [
                        (f"/summary/{id_1}", data[2], status200), 
                        (f"/summary/{id_2}", data[0], status200), 
                        (f"/summary/{id_3}", data[1], status200),
                        (f"/summary/{id_3}", data[3], status422),
                        (f"/summary/-1", data[0], status404)
                        ])
def test_update_record(url, data, status_code):
    response = client.put(url, json=data)
    assert response.status_code == status_code


# Test delete record
@pytest.mark.parametrize("url,status_code", [
                        (f"/summary/{id_1}", status200), 
                        (f"/summary/-1", status404)
                        ])
def test_delete_record(url, status_code):
    response = client.delete(url)
    assert response.status_code == status_code


# Test get global summary record
@pytest.mark.parametrize("url,status_code", [
                        ("/summary/global?start_date=2021-07-11&end_date=2021-07-11", status200), 
                        ("/summary/global?start_date=2201-07-11&end_date=2021-07-11", status400),
                        ("/summary/global?start_date=2021-07-11&end_date=2021-04-04", status400),
                        ("/summary/global?start_date=abc&end_date=def", status422),
                        ("/summary/global?start_date=2019-12-01&end_date=2019-12-30", status404),
                        ])
def test_get_global_summary(url, status_code):
    response = client.get(url)
    assert response.status_code == status_code


# Test get country summary record
@pytest.mark.parametrize("url,status_code", [
                        ("/summary/country?country=Singapore&start_date=2021-07-11&end_date=2021-07-11", status200), 
                        ("/summary/country?country=Singapore&start_date=2201-07-11&end_date=2021-07-11", status400),
                        ("/summary/country?country=Singapore&start_date=2021-07-11&end_date=2021-04-04", status400),
                        ("/summary/country?country=Singapore&start_date=abc&end_date=def", status422),
                        ("/summary/country?country=Singapore&start_date=2019-12-01&end_date=2019-12-30", status404),
                        ("/summary/country?country=abc&start_date=2019-12-01&end_date=2019-12-30", status404),
                        ])
def test_get_country_summary(url, status_code):
    response = client.get(url)
    assert response.status_code == status_code


# Test get global daily record
@pytest.mark.parametrize("url,status_code", [
                        ("/daily/global?start_date=2021-07-11&end_date=2021-07-11", status200), 
                        ("/daily/global?start_date=2201-07-11&end_date=2021-07-11", status400),
                        ("/daily/global?start_date=2021-07-11&end_date=2021-04-04", status400),
                        ("/daily/global?start_date=abc&end_date=def", status422),
                        ("/daily/global?start_date=2019-12-01&end_date=2019-12-30", status404),
                        ])
def test_get_global_summary(url, status_code):
    response = client.get(url)
    assert response.status_code == status_code


# Test get country daily record
@pytest.mark.parametrize("url,status_code", [
                        ("/daily/country?country=Singapore&start_date=2021-07-11&end_date=2021-07-11", status200), 
                        ("/daily/country?country=Singapore&start_date=2201-07-11&end_date=2021-07-11", status400),
                        ("/daily/country?country=Singapore&start_date=2021-07-11&end_date=2021-04-04", status400),
                        ("/daily/country?country=Singapore&start_date=abc&end_date=def", status422),
                        ("/daily/country?country=Singapore&start_date=2019-12-01&end_date=2019-12-30", status404),
                        ("/daily/country?country=abc&start_date=2019-12-01&end_date=2019-12-30", status404),
                        ])
def test_get_country_summary(url, status_code):
    response = client.get(url)
    assert response.status_code == status_code


