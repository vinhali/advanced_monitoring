#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# filename: ConsumptionAnalysisNeuralNetwork.py
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
# 1.0.0 31-03-2020      Inital version
#
#-----------------------------------------------------------------------------------------------------------
try:
    import pandas as pd
    import psycopg2
    import requests
    import json
    from requests.auth import HTTPBasicAuth
    import time
    import tensorflow as tf
    import numpy as np
    from sklearn.metrics import mean_absolute_error
    from datetime import datetime
    import sys
except ImportError as e:
    print("[ALERT] Error import caused by: {}".format(e))
    sys.exit()

class initTraining():

    def startProcessing(self):

        init = neuralAnalisys()
        init.getValuesMemory()

class neuralAnalisys():

    def getValuesMemory(self):

        dataSet = []
        start = neuralAnalisys()

        try:

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            api_URL = 'http://127.0.0.1:5000/getMemory'

            try:
                response = requests.get(api_URL, auth=HTTPBasicAuth('root', 'root'), headers=headers)
                response_data = response.json()
            except:
                print("[ALERT] Error caused by credentials or request")

            for line in response_data:
                dataSet.append(np.array([line['datecollect']['$date'],line['hostname'],line['historyvalue']]))

            return start.neuralTraining(dataSet)

        except Exception as e:
            print("[ERROR] Error caused by: {}".format(e))

    def neuralTraining(self, dataSet):

        send = neuralAnalisys()

        try:

            datecollect = [x[0] for x in dataSet]
            servers = [x[1] for x in dataSet]
            valuesAnalisys = [float(x[2]) for x in dataSet]

            base = np.array(valuesAnalisys)

            periods = len(valuesAnalisys) - 1
            future_forecast = 1

            X = base[0:(len(base) - (len(base) % periods))]
            X_batches = X.reshape(-1, periods, 1)

            y = base[1:(len(base) - (len(base) % periods)) + future_forecast]
            y_batches = y.reshape(-1, periods, 1)

            X_test = base[-(periods + future_forecast):]
            X_test = X_test[:periods]
            X_test = X_test.reshape(-1, periods, 1)
            y_test = base[-(periods):]
            y_test = y_test.reshape(-1, periods, 1)

            tf.reset_default_graph()

            appetizer = 1
            hidden_neurons = 100
            exit_neurons = 1

            xph = tf.placeholder(tf.float32, [None, periods, appetizer])
            yph = tf.placeholder(tf.float32, [None, periods, exit_neurons])

            cell = tf.contrib.rnn.BasicRNNCell(num_units = hidden_neurons, activation = tf.nn.relu)

            cell = tf.contrib.rnn.OutputProjectionWrapper(cell, output_size = 1)

            exit_rnn, _ = tf.nn.dynamic_rnn(cell, xph, dtype = tf.float32)
            calculateError = tf.losses.mean_squared_error(labels = yph, predictions = exit_rnn)
            otimizador = tf.train.AdamOptimizer(learning_rate = 0.001)
            training = otimizador.minimize(calculateError)

            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                
                for epoch in range(1000):
                    _, cost = sess.run([training, calculateError], feed_dict = {xph: X_batches, yph: y_batches})
                    if epoch % 100 == 0:
                        print("[INFO] Epoch: {} - Level Error: {}".format(epoch,cost))
                
                forecast = sess.run(exit_rnn, feed_dict = {xph: X_test})

            y_test.shape
            y_test2 = np.ravel(y_test)

            final_forecast = np.ravel(forecast)

            mae = mean_absolute_error(y_test2, final_forecast)

            errorLevel = str(mae)

            dataModeling = list(zip(servers, final_forecast, valuesAnalisys, errorLevel, datecollect))

            for servers, final_forecast, valuesAnalisys, errorLevel, datecollect in dataModeling:
                send.postForecastMemory(servers, final_forecast, errorLevel, datecollect)

        except Exception as e:
            print("[ERROR] Error caused by: {}".format(e))

    def postForecastMemory(self,hostname,memory,lvlerror,collected):
        try:

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            api_URL_SET = 'http://127.0.0.1:5000/setForecastMemory'

            payload = {"server": "{}".format(hostname), 
                        "forecastmemory": "{}".format(memory), 
                        "levelerror": "{}".format(lvlerror), 
                        "datecollect": collected}

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
