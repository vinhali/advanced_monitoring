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

CREATE TABLE "CI" (
  "countci" SERIAL NOT NULL,
  "idci" int PRIMARY KEY NOT NULL,
  "ip" varchar NOT NULL,
  "customer" varchar NOT NULL,
  "customer_code" varchar NOT NULL,
  "hostname" varchar NOT NULL,
  "dateci" timestamp NOT NULL
);

CREATE TABLE "EXPORTZABBIX" (
  "countexportzabbix" SERIAL,
  "id" SERIAL,
  "fk_exportzabbix" int PRIMARY KEY NOT NULL,
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
  "fk_impact" int PRIMARY KEY NOT NULL,
  "sla" varchar NOT NULL,
  "impact" varchar NOT NULL,
  "estimativemoney" varchar NOT NULL,
  "downtime" varchar NOT NULL,
  "contract" varchar NOT NULL,
  "felling" varchar NOT NULL,
  "dateimpact" timestamp NOT NULL
);

CREATE TABLE "FORECAST" (
  "countforecast" SERIAL,
  "fk_forecast" int PRIMARY KEY NOT NULL,
  "forecastmemory" varchar NOT NULL,
  "forecastcpu" varchar NOT NULL,
  "forecastcapacity" varchar NOT NULL,
  "forecastuptime" varchar NOT NULL,
  "levelerror" varchar NOT NULL,
  "datecollect" timestamp NOT NULL,
  "dateforecast" timestamp NOT NULL
);

CREATE TABLE "RELATIONSHIP" (
  "countrelationship" SERIAL,
  "fk_relationship" int PRIMARY KEY NOT NULL,
  "sector" varchar NOT NULL,
  "location" varchar NOT NULL,
  "type" varchar NOT NULL,
  "journey" varchar NOT NULL,
  "user" varchar NOT NULL,
  "number_thrist" varchar NOT NULL,
  "officejob" varchar NOT NULL,
  "daterelationship" timestamp NOT NULL
);

CREATE TABLE "DESCRIPTION" (
  "countdescription" SERIAL,
  "fk_description" int PRIMARY KEY NOT NULL,
  "whoami" varchar NOT NULL,
  "application" varchar NOT NULL,
  "topology" varchar NOT NULL,
  "so" varchar NOT NULL,
  "support" varchar NOT NULL,
  "architeture" varchar NOT NULL,
  "capacity" varchar NOT NULL,
  "memory" varchar NOT NULL,
  "number_cpu" varchar NOT NULL,
  "version" varchar NOT NULL,
  "latency" varchar NOT NULL,
  "network" varchar NOT NULL,
  "vpn" varchar NOT NULL,
  "cpu" varchar NOT NULL,
  "monitoring" varchar NOT NULL,
  "inbound" varchar NOT NULL,
  "outbound" varchar NOT NULL,
  "uptime" varchar NOT NULL,
  "datedescription" timestamp NOT NULL
);

CREATE TABLE "CUSTOMER" (
  "countcustomer" SERIAL,
  "idcustomer" varchar PRIMARY KEY NOT NULL,
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

ALTER TABLE "EXPORTZABBIX" ADD FOREIGN KEY ("fk_exportzabbix") REFERENCES "CI" ("idci");

ALTER TABLE "IMPACT" ADD FOREIGN KEY ("fk_impact") REFERENCES "CI" ("idci");

ALTER TABLE "FORECAST" ADD FOREIGN KEY ("fk_forecast") REFERENCES "CI" ("idci");

ALTER TABLE "RELATIONSHIP" ADD FOREIGN KEY ("fk_relationship") REFERENCES "CI" ("idci");

ALTER TABLE "DESCRIPTION" ADD FOREIGN KEY ("fk_description") REFERENCES "CI" ("idci");

ALTER TABLE "CUSTOMER" ADD FOREIGN KEY ("idcustomer") REFERENCES "CI" ("idci");
