-- Create table

CREATE TABLE IF NOT EXISTS records (
	id SERIAL PRIMARY KEY,
	province_state VARCHAR(255),
	country_region VARCHAR(255) NOT NULL,
	latitude DOUBLE PRECISION,
	longitude DOUBLE PRECISION,
	date DATE NOT NULL,
	confirmed INT,
	deaths INT,
	recovered INT,
	active INT,
	new_confirmed INT,
	new_deaths INT,
	new_recovered INT,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS country (
	country_id SERIAL PRIMARY KEY,
	country VARCHAR(255) NOT NULL
);
