#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# filename: getValues.py
#-----------------------------------------------------------------------------------------------------------
# Introduction
# Script to be used in advanced monitoring
#
#-----------------------------------------------------------------------------------------------------------
# Copyright
#
# Copyright (C) 1989, 1991 Free Software Foundation, Inc., [http://fsf.org/]
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.
#
#-----------------------------------------------------------------------------------------------------------
# Version:      1.0.0
# Author:       Luis Henrique Vinhali <vinhali@outlook.com>
#
# Changelog:
# 1.0.0 02-02-2020      Inital version
#
#-----------------------------------------------------------------------------------------------------------

from zabbix.api import ZabbixAPI
import psycopg2
from datetime import datetime, date, time, timedelta

zapi = ZabbixAPI(url='http://192.168.1.135/zabbix', user='Admin', password='zabbix')

# Connection with postgres
connpostgres = psycopg2.connect("host='127.0.0.1'"
                        " dbname='networkneural'"
                        " user='postgres'"
			" password='postgres'")
cursorpost = connpostgres.cursor()

# date now - 1 
d = date.today() - timedelta(days = 0)

# date + 0:00
startTimestamp = int(datetime.combine(d, time(0, 0)).timestamp())
# date + 23:59
endTimestamp = int(datetime.combine(d, time(23, 59)).timestamp())

groupFilter = {'name': 'Servers Production'}
itemFilter = {'name': 'Memória em uso (Porcentagem)'}

# Get the hostgroup id by its name 
hostgroups = zapi.hostgroup.get(filter=groupFilter, output=['groupids', 'name'])

# Get the hosts of the hostgroup by hostgroup id
hosts = zapi.host.get(groupids=hostgroups[0]['groupid'])

for host in hosts:
    # Get the item info (not the values!) by item name AND host id
    items = zapi.item.get(filter=itemFilter, host=host['host'], output='extend', selectHosts=['host', 'name'])

    # for loop - for future fuzzy search, otherwise don't loop and use items[0] 
    for item in items:
        # Get item values
        values = zapi.history.get(itemids=item['itemid'], time_from=startTimestamp, time_till=endTimestamp, history=item['value_type'])
        # print history values
        for historyValue in values:
            cursorpost.execute("INSERT INTO dataset (hostname,itemid,itemname,itemkey,historyvalue,datecollect,dateinsert) VALUES ('{}', '{}', '{}', '{}', '{}', \'"
                  .format(
                host['host'],
                item['itemid'],
                item['name'],
                item['key_'],
                historyValue['value'])
                +str(datetime.utcfromtimestamp(int(historyValue['clock'])).strftime('%Y-%m-%d %H:%M:%S'))+"\', current_timestamp);")
            
connpostgres.commit()
cursorpost.close()
connpostgres.close()
			

