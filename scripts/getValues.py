from zabbix.api import ZabbixAPI
import psycopg2
from datetime import datetime, date, time, timedelta

zapi = ZabbixAPI(url='http://192.168.1.250/zabbix', user='Admin', password='zabbix')

# Connection with postgres
connpostgres = psycopg2.connect("host='192.168.1.250'"
                        " dbname='networkneural'"
                        " user='postgres'"
			" password=postgres")
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
			