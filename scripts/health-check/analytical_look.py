#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# filename: analytical_look.py
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
# 1.0.0 10-04-2020      Inital version
#
#-----------------------------------------------------------------------------------------------------------
try:
    import sys
    import os
    import time
    import requests
    import json
    import psycopg2
    import operator
    import numpy as np
    import pandas as pd
    from datetime import datetime
    from requests.auth import HTTPBasicAuth
except ImportError as e:
    print("[ALERT] Error import caused by: {}".format(e))
    sys.exit()

class initTraining():

    def startProcessing(self):

        init = neuralAnalisys()
        init.getValuesMemory()
        init.getValuesCpu()

class neuralAnalisys():

    def getValuesMemory(self):

        dataSet = []
        start = neuralAnalisys()

        try:

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            api_URL = 'http://127.0.0.1:5000/getForecastMemory'

            try:
                response = requests.get(api_URL, auth=HTTPBasicAuth('root', 'root'), headers=headers)
                response_data = response.json()
            except:
                print("[ALERT] Error caused by credentials or request")

            for line in response_data:
                dataSet.append(np.array([line['server'],line['forecastmemory'],line['levelerror'],line['datecollect']['$date']]))

            return start.crisisAnalytics(dataSet,'Memory')

        except Exception as e:
            print("[ERROR] Error caused by: {}".format(e))

    def getValuesCpu(self):
    
        dataSet = []
        start = neuralAnalisys()

        try:

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            api_URL = 'http://127.0.0.1:5000/getForecastCpu'

            try:
                response = requests.get(api_URL, auth=HTTPBasicAuth('root', 'root'), headers=headers)
                response_data = response.json()
            except:
                print("[ALERT] Error caused by credentials or request")

            for line in response_data:
                dataSet.append(np.array([line['server'],line['forecastcpu'],line['levelerror'],line['datecollect']['$date']]))

            return start.crisisAnalytics(dataSet,'CPU')

        except Exception as e:
            print("[ERROR] Error caused by: {}".format(e))

    def crisisAnalytics(self, dataSet, name):

        send = neuralAnalisys()

        try:

            valuesAnalisys = [float(x[1]) for x in dataSet]

            crisisLimit = max(enumerate(valuesAnalisys), key=operator.itemgetter(1))

            for consume in dataSet:
                if float(crisisLimit[1]) >= 80:
                    if float(consume[1]) == float(crisisLimit[1]):
                        print("[INFO] {0} Crisis: {1}".format(name,consume))
                        os.system('''php /etc/neural/tickets/open.php eventhost="{}" event="OPEN" state="CRITICAL" hostproblemid=0 lasthostproblemid=0 servico="{}" triggerid="Forecast - " eventansible="Analytical Crisis"'''.format(
                        consume[0],str("{} with Consume > 80% for {} - Level Error: {} - When: {}").format(
                                name,consume[0],consume[2],consume[3])
                        ))
                        send.postForecastGrafana(consume[0], name, consume[1], consume[3], consume[2])

        except Exception as e:
            print("[ERROR] Error caused by: {}".format(e))

    def postForecastGrafana(self,hostname,typeAnalisys,tresholdAnalisys,lossup,levelError):
        try:

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            api_URL_SET = 'http://127.0.0.1:5000/setForecastGrafana'

            payload = {"hostname": "{}".format(hostname), 
                        "typeAnalisys": "{}".format(typeAnalisys), 
                        "tresholdAnalisys": "{}".format(tresholdAnalisys),
                        "lossup": "{}".format(lossup),
                        "levelError": "{}".format(levelError)}

            r = requests.post(api_URL_SET, auth=HTTPBasicAuth('root', 'root'), data=json.dumps(payload), headers=headers)
            
            if(r.status_code == 200):
                print("[INFO] Data insert status: {}".format(r.status_code))
            else:
                print("[INFO] Data insert status: {}".format(r.status_code))

        except Exception as e:

            print("[ALERT] Error caused by {}".format(e))

if __name__ == "__main__":
    
    flow = initTraining()
    flow.startProcessing()
