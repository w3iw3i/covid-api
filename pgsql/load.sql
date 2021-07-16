-- Insert records from csv
COPY records (province_state, country_region, latitude, longitude, date, confirmed, deaths, recovered, active, new_confirmed, new_deaths, new_recovered) FROM '/data/master.csv' with DELIMITER ',' CSV HEADER;


-- Import country from csv
COPY country (country) FROM '/data/country.csv' with DELIMITER ',' CSV HEADER;