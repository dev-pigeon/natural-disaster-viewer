CREATE TABLE disasters (
    id varchar(255) PRIMARY KEY,
    disaster_type varchar(255) NOT NULL,
    begin_date varchar(255) NOT NULL,
    end_date varchar(255) NOT NULL,
    fips_code varchar (255) NOT NULL,
    latitude varchar(255) NOT NULL,
    longitude varchar(255) NOT NULL
);