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

class neuralAnalisys():

    def getValuesAPI(self):

        dataSet = []

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

        except Exception as e:
            print("[ERROR] Error caused by: {}".format(e))

        return dataSet

    def neuralTraining(self):

        try:

            neural = neuralAnalisys()
            dataSet = neural.getValuesAPI()

            datecollect = [x[0] for x in dataSet]
            servers = [x[1] for x in dataSet]
            historyoriginal = [float(x[2]) for x in dataSet]
            #del historyoriginal[1]

            base = np.array(historyoriginal)

            periodos = len(historyoriginal) - 1
            previsao_futura = 1 # horizonte

            X = base[0:(len(base) - (len(base) % periodos))]
            X_batches = X.reshape(-1, periodos, 1)

            y = base[1:(len(base) - (len(base) % periodos)) + previsao_futura]
            y_batches = y.reshape(-1, periodos, 1)

            X_teste = base[-(periodos + previsao_futura):]
            X_teste = X_teste[:periodos]
            X_teste = X_teste.reshape(-1, periodos, 1)
            y_teste = base[-(periodos):]
            y_teste = y_teste.reshape(-1, periodos, 1)

            tf.reset_default_graph()

            entradas = 1
            neuronios_oculta = 100
            neuronios_saida = 1

            xph = tf.placeholder(tf.float32, [None, periodos, entradas])
            yph = tf.placeholder(tf.float32, [None, periodos, neuronios_saida])

            celula = tf.contrib.rnn.BasicRNNCell(num_units = neuronios_oculta, activation = tf.nn.relu)
            # camada saida
            celula = tf.contrib.rnn.OutputProjectionWrapper(celula, output_size = 1)

            saida_rnn, _ = tf.nn.dynamic_rnn(celula, xph, dtype = tf.float32)
            erro = tf.losses.mean_squared_error(labels = yph, predictions = saida_rnn)
            otimizador = tf.train.AdamOptimizer(learning_rate = 0.001)
            treinamento = otimizador.minimize(erro)

            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                
                for epoca in range(200):
                    _, custo = sess.run([treinamento, erro], feed_dict = {xph: X_batches, yph: y_batches})
                    if epoca % 100 == 0:
                        print(epoca + 1, ' Error: ', custo)
                
                previsoes = sess.run(saida_rnn, feed_dict = {xph: X_teste})
            y_teste.shape
            y_teste2 = np.ravel(y_teste)

            previsoes2 = np.ravel(previsoes)

            # level error
            mae = mean_absolute_error(y_teste2, previsoes2)

            # Unindo valores originais com previstos e fazendo insert
            errorLevel = str(mae)
            #dataModeling = map(lambda e: (dateTimeObj, e, errorLevel), previsoes2)
            dataModeling = list(zip(previsoes2, historyoriginal, datecollect, servers))

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            api_URL_SET = 'http://127.0.0.1:5000/setForecast'

            for prev, ori, collect, srv in dataModeling:
                print("INSERT into forecastmemoryconsumption (date, forecastvalue, originalValue, datecollect, hostname, levelerror) VALUES (current_timestamp, '{}', '{}', '{}', '{}', '{}')".format(prev, ori, collect, srv, errorLevel))

            # testing
            try:

                payload = {"idci": "12525", "forecastmemory": "90", "forecastcpu": "85",
                            "forecastcapacity": "85","forecastuptime": "85","levelerror": "85",
                            "datecollect": "2020-04-01","dateforecast": "2020-04-01"}

                r = requests.post(api_URL_SET, auth=HTTPBasicAuth('root', 'root'), data=json.dumps(payload), headers=headers)
                print(r.status_code)

            except:

                print("[ALERT] Error caused by credentials or request")

        except Exception as e:
            print("[ERROR] Error caused by: {}".format(e))

if __name__ == "__main__":
    
    flow = neuralAnalisys()
    flow.neuralTraining()
