CREATE DATABASE networkNeural;

CREATE TABLE dataSet(
    id SERIAL,
    hostname varchar(100),
    itemid varchar(100),
    itemname varchar(100),
    itemkey varchar(100),
    historyvalue varchar(100),
    datecollect varchar(100),
    dateinsert timestamp
);


CREATE TABLE ForecastMemoryConsumption(
    id SERIAL,
    date timestamp,
    forecastValue varchar(20),
    originalValue varchar(20)
);