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
try:
    from zabbix.api import ZabbixAPI
    from datetime import datetime, date, time, timedelta
    import requests
    import json
    import subprocess
    import sys
    import psycopg2
except ImportError as e:
    print("[INFO] Error import caused by: {}".format(e))

class exportDataAPIzabbix():

    def loginAPI(self, urlZB, userZB, passZB, groupHost, itemZB, rangeDay, adressDB, dbName, userDB, passDB):

        # Header API
        ZABIX_ROOT = urlZB
        url = ZABIX_ROOT + '/api_jsonrpc.php'

        payload = {
            "jsonrpc" : "2.0",
            "method" : "user.login",
            "params": {
            'user': userZB,
            'password': passZB,
            },
            "auth" : None,
            "id" : 0,
        }

        headers = {
            'content-type': 'application/json',
        }

        try:

            # Method use API
            zapi = ZabbixAPI(url=urlZB, user=userZB, password=passZB)
            # Test connection with API
            requestZB = requests.post(url, data=json.dumps(payload), headers=headers)
            resultZB = requestZB.json()
            json.dumps(resultZB)

            print("[INFO] API connected")
            print("[INFO] jsonrpc: {} && result: {}".format(resultZB['jsonrpc'],resultZB['result']))

            startCollect = exportDataAPIzabbix()
            return startCollect.collectAPI(zapi, groupHost, itemZB, rangeDay, adressDB, dbName, userDB, passDB)

        except Exception as e:

            print("[INFO] API not connected")
            print("Zabbix URL Error: {}".format(e))

            sys.exit()

    def connectPGSQL(self,host,itemid,itemname,itemkey,historyvalue,clock, adressDB, dbName, userDB, passDB):

        try:

            # Create connection adressDB, dbName, userDB, passDB
            connpostgres = psycopg2.connect("host='{}'"
                                    " dbname='{}'"
                                    " user='{}'"
                        " password='{}'".format(adressDB, dbName, userDB, passDB))
            cursorpost = connpostgres.cursor()
            # Insert data collect
            cursorpost.execute('''INSERT INTO "MEMORYEXPORTZB" (hostname,itemid,itemname,
            itemkey,historyvalue,datecollect,dateinsert) 
            VALUES ('{}', '{}', '{}', '{}', '{}', \''''.format(
            host,
            itemid,
            itemname,
            itemkey,
            historyvalue)
            +str(datetime.utcfromtimestamp(int(clock)).strftime('%Y-%m-%d %H:%M:%S'))+
            "\',current_timestamp);")
            # End connections in pgsql
            connpostgres.commit()
            cursorpost.close()
            connpostgres.close()

        except Exception as e:

            print("Error insert data caused by: {}".format(e))
            sys.exit()

    def collectAPI(self, zapi, groupHost, itemZB, rangeDay, adressDB, dbName, userDB, passDB):

        try:

            # date now - 1 
            d = date.today() - timedelta(days = rangeDay)

            # date + 0:00
            startTimestamp = int(datetime.combine(d, time(0, 0)).timestamp())
            # date + 23:59
            endTimestamp = int(datetime.combine(d, time(23, 59)).timestamp())

            groupFilter = {'name': groupHost}
            itemFilter = {'name': itemZB}

            # Get the hostgroup id by its name 
            hostgroups = zapi.hostgroup.get(filter=groupFilter, output=['groupids', 'name'])

            # Get the hosts of the hostgroup by hostgroup id
            hosts = zapi.host.get(groupids=hostgroups[0]['groupid'])

            for host in hosts:
                # Get the item info (not the values!) by item name AND host id
                items = zapi.item.get(filter=itemFilter, host=host['host'], output='extend', selectHosts=['host', 'name'])

                # for loop - for future fuzzy search, otherwise don't loop and use items[0] 
                for item in items:
                    # Get item values range or all
                    values = zapi.history.get(itemids=item['itemid'], time_from=startTimestamp, time_till=endTimestamp, history=item['value_type'])
                    #values = zapi.history.get(itemids=item['itemid'], history=item['value_type'])

                    for historyValue in values:
                        #print(host['host'],item['itemid'],item['name'],item['key_'],historyValue['value'],str(datetime.utcfromtimestamp(int(historyValue['clock'])).strftime('%Y-%m-%d %H:%M:%S')))
                        # insert values in database
                        insertData = exportDataAPIzabbix()
                        insertData.connectPGSQL(host['host'],item['itemid'],item['name'],item['key_'],historyValue['value'],historyValue['clock'], adressDB, dbName, userDB, passDB)

            print("[INFO] Values ​​collected by the API")        
            print("[INFO] Values ​​entered in the database")
            print("[INFO] End connection PGSQL")
            print("[INFO] End script")
            print("[STATUS] Everything happened successfully [ok]")

        except Exception as e:

            print("Error collect API caused by: {}".format(e))
            sys.exit()

if __name__ == "__main__":
    
    flow = exportDataAPIzabbix()
    flow.loginAPI('http://192.168.1.135/zabbix', 'Admin', 'zabbix', 
                'Servers Production', 'Memória em uso (Porcentagem)', 
                0, '127.0.0.1', 'networkneural', 'postgres', 'postgres')

    #flow.loginAPI(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],
    #sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10]) # Send external command python

# login API respective values:
# Value1 1 --> URL ZABBIX
# Value1 2 --> USER ZABBIX
# Value1 3 --> PASSWORD ZABBIX
# Value1 4 --> GROUP OF HOSTS ZABBIX FOR COLLECT
# Value1 5 --> ITEM ZABBIX FOR COLLECT
# Value1 6 --> RANGE OF COLLECT (DAY) 0 = date actual
