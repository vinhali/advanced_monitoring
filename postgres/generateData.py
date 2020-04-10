import random
import psycopg2
from datetime import datetime, timedelta

def connectPgsql():

    try:

        conn = psycopg2.connect("dbname='networkneural' user='postgres' host='192.168.1.138' password='postgres'")
        cur = conn.cursor()

        return cur, conn

    except Exception as e:

        print("[FAILED] {}".format(e))

def datetime_range(start,end,delta):
    current = start
    while current < end:
        yield current
        current += delta

def generatePercent(start,end,lengthArray):

    n = 0
    a = []

    try:

        while n <= lengthArray:
            n = n+1
            a.append(random.uniform(start, end))
        print("[SUCESS] Created array random - Lenght: {0} - Range ({1},{2})".format(lengthArray,start,end))

        return a

    except Exception as e:

        print("[FAILED] {}".format(e))

def generateQuery(tbl,hostname,itemid,itemname,itemkey,days,month,year,hourStart,endTime):

    try:

        cur, conn = connectPgsql()

        dts = [dt.strftime('%Y-%m-%d %H:%M') for dt in 
        datetime_range(datetime(int(year), int(month), int(days), int(hourStart)), 
        datetime(int(year), int(month), int(days), int(endTime)), 
        timedelta(minutes=1))]

        cpuMin = generatePercent(20,40,500)
        cpuMed = generatePercent(50,70,300)
        cpuMax = generatePercent(70,100,220)
        joinedlist = cpuMin + cpuMax + cpuMed

        for val1,va2 in zip(joinedlist,dts):

            stringQuery = '''INSERT INTO "{0}" 
            (hostname,itemid,itemname,itemkey,historyvalue,datecollect,dateinsert) 
            VALUES ('{1}','{2}','{3}','{4}','{5}','{6}',current_timestamp)'''.format(
            tbl,hostname,itemid,itemname,itemkey,val1,va2)
            cur.execute(stringQuery)

        conn.commit()
        conn.close()

        print("[SUCESS] Data inserted")
        print("[INFO] Data - Lenght: {}".format(len(dts)))

    except Exception as e:

        print("[FAILED] {}".format(e))

def run(days,month,year,hourStart,endTime):

    try:

        generateQuery('CPUEXPORTZB','serveNFE','30517','Uso do processador na média de 1 minuto','system.cpu.load[percpu,avg1]',days, month, year, hourStart, endTime)
        generateQuery('MEMORYEXPORTZB','serveNFE','31530','Memória em uso (Porcentagem)','vm.memory.size[pused]',days, month, year, hourStart, endTime)

    except Exception as e:

        print("[FAILED] {}".format(e))

if __name__ == '__main__':

    for days in range(8):
        run(days, 4, 2020, 6, 23)
