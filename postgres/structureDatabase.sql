-------------------------------------------------------------------------------------------------------------
-- filename: structureDatabase.sql
-- Introduction
-- Script to be used in advanced monitoring
--
-------------------------------------------------------------------------------------------------------------
-- Copyright
--
-- Copyright (C) 1989, 1991 Free Software Foundation, Inc., [http://fsf.org/]
-- 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
-- Everyone is permitted to copy and distribute verbatim copies
-- of this license document, but changing it is not allowed.
--
-------------------------------------------------------------------------------------------------------------
-- Version:      1.0.0
-- Author:       Luis Henrique Vinhali <vinhali@outlook.com>
--
-- Changelog:
-- 1.0.0 02-02-2020      Inital version
--
-------------------------------------------------------------------------------------------------------------

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
