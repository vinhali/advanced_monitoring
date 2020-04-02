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

CREATE DATABASE networkneural;


CREATE TABLE "CI" (
  "countci" SERIAL NOT NULL,
  "idci" varchar PRIMARY KEY NOT NULL,
  "ip" varchar NOT NULL,
  "customer" varchar NOT NULL,
  "customer_code" varchar NOT NULL,
  "hostname" varchar NOT NULL,
  "dateci" timestamp NOT NULL
);

CREATE TABLE "EXPORTZABBIX" (
  "countexportzabbix" SERIAL,
  "id" SERIAL,
  "idci" varchar PRIMARY KEY NOT NULL,
  "hostname" varchar NOT NULL,
  "itemid" varchar NOT NULL,
  "itemname" varchar NOT NULL,
  "itemkey" varchar NOT NULL,
  "historyvalue" varchar NOT NULL,
  "datecollect" varchar NOT NULL,
  "dateinsert" timestamp NOT NULL,
  "datezabbix" timestamp NOT NULL
);

CREATE TABLE "IMPACT" (
  "countimpact" SERIAL,
  "idci" varchar PRIMARY KEY NOT NULL,
  "sla" varchar NOT NULL,
  "impact" varchar NOT NULL,
  "estimativemoney" varchar NOT NULL,
  "downtime" varchar NOT NULL,
  "felling" varchar NOT NULL,
  "dateimpact" timestamp NOT NULL
);

CREATE TABLE "RELATIONSHIP" (
  "countrelationship" SERIAL,
  "idci" varchar PRIMARY KEY NOT NULL,
  "sector" varchar NOT NULL,
  "location" varchar NOT NULL,
  "type" varchar NOT NULL,
  "journey" varchar NOT NULL,
  "user" varchar NOT NULL,
  "number_thrist" varchar NOT NULL,
  "daterelationship" timestamp NOT NULL
);

CREATE TABLE "DESCRIPTION" (
  "countdescription" SERIAL,
  "idci" varchar PRIMARY KEY NOT NULL,
  "whoami" varchar,
  "application" varchar NOT NULL,
  "topology" varchar NOT NULL,
  "so" varchar,
  "support" varchar NOT NULL,
  "architeture" varchar,
  "capacity" varchar,
  "memory" varchar,
  "number_cpu" varchar,
  "version" varchar,
  "latency" varchar,
  "network" varchar,
  "vpn" varchar,
  "cpu" varchar,
  "monitoring" varchar,
  "inbound" varchar,
  "outbound" varchar,
  "uptime" varchar,
  "datedescription" timestamp NOT NULL
);

CREATE TABLE "CUSTOMER" (
  "countcustomer" SERIAL,
  "customer_code" varchar NOT NULL,
  "customer" varchar NOT NULL,
  "segment" varchar NOT NULL,
  "cnpj" varchar NOT NULL,
  "socialreason" varchar NOT NULL,
  "contact" varchar NOT NULL,
  "telephone" varchar NOT NULL,
  "adress" varchar NOT NULL,
  "datecustomer" timestamp NOT NULL
);
  
CREATE TABLE "PLAYBOOK"(
id serial primary key,
name varchar not null,
goal varchar not null,
date_insert timestamp
);

CREATE TABLE "ANSIBLE_HISTORY"(
id serial primary key,
idoPeration int not null
playbook varchar not null,
technican varchar,
status varchar not null,
frequency varchar not null,
customer varchar not null,
host varchar not null,
startdate timestamp
)

CREATE TABLE "MEMORYEXPORTZB"(
hostname varchar,
itemid int,
itemname varchar,
itemkey varchar,
historyvalue real,
datecollect timestamp,
dateinsert timestamp
);

CREATE TABLE "FORECASTMEMORY" (
  "countforecast" SERIAL PRIMARY KEY,
  "server" varchar NOT NULL,
  "forecastmemory" varchar NOT NULL,
  "levelerror" varchar NOT NULL,
  "datecollect" timestamp NOT NULL,
  "dateforecast" timestamp NOT NULL
);

CREATE TABLE "CPUEXPORTZB"(
hostname varchar,
itemid int,
itemname varchar,
itemkey varchar,
historyvalue real,
datecollect timestamp,
dateinsert timestamp
);

CREATE TABLE "FORECASTCPU" (
  "countforecast" SERIAL PRIMARY KEY,
  "server" varchar NOT NULL,
  "forecastcpu" varchar NOT NULL,
  "levelerror" varchar NOT NULL,
  "datecollect" timestamp NOT NULL,
  "dateforecast" timestamp NOT NULL
);

CREATE TABLE "DISKEXPORTZB"(
hostname varchar,
itemid int,
itemname varchar,
itemkey varchar,
historyvalue real,
datecollect timestamp,
dateinsert timestamp
);

CREATE TABLE "FORECASTDISK" (
  "countforecast" SERIAL PRIMARY KEY,
  "server" varchar NOT NULL,
  "forecastdisk" varchar NOT NULL,
  "levelerror" varchar NOT NULL,
  "datecollect" timestamp NOT NULL,
  "dateforecast" timestamp NOT NULL
);
