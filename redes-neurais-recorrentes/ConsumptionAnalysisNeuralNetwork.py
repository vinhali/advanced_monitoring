#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# filename: tresholdDetector.py
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

import pandas as pd
import psycopg2

#base = pd.read_csv('dados-hardware.csv')

# CRIANDO CONEXAO NO PSQL                                                                                                                                                                                           
conn = psycopg2.connect(host="192.168.1.250", dbname='networkneural', user='postgres', password='postgres')
cur = conn.cursor()
sql = 'SELECT DISTINCT ON (date_trunc(\'hour\', to_timestamp(datecollect, \'YYYY-MM-DD hh24:mi:ss\')::timestamp))  \
id,                                                                                                                 \
date_trunc(\'hour\', to_timestamp(datecollect, \'YYYY-MM-DD hh24:mi:ss\')::timestamp) as Time,                       \
historyvalue::numeric::float,                                                                                       \
hostname                                                                                                               \
FROM dataset                                                                                                            \
WHERE hostname = \'vinhali\'                                                                                             \
ORDER BY date_trunc(\'hour\', to_timestamp(datecollect, \'YYYY-MM-DD hh24:mi:ss\')::timestamp),                           \
to_timestamp(datecollect, \'YYYY-MM-DD hh24:mi:ss\')::timestamp;                                                           \
'
cur.execute(sql)
dataSet = cur.fetchall()

datecollect = [x[1] for x in dataSet]
servers = [x[3] for x in dataSet]
historyoriginal = [x[2] for x in dataSet]
del historyoriginal[1]

base = pd.read_sql(sql, conn)

cur.close()
conn.close()

base = base.dropna()
base = base.iloc[:,2].values

periodos = 19
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

import tensorflow as tf
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
    
    for epoca in range(2000):
        _, custo = sess.run([treinamento, erro], feed_dict = {xph: X_batches, yph: y_batches})
        if epoca % 100 == 0:
            print(epoca + 1, ' erro: ', custo)
    
    previsoes = sess.run(saida_rnn, feed_dict = {xph: X_teste})
    
import numpy as np
y_teste.shape
y_teste2 = np.ravel(y_teste)

previsoes2 = np.ravel(previsoes)

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_teste2, previsoes2)

from datetime import datetime

# data e hora
dateTimeObj = str(datetime.now())

# Unindo valores originais com previstos e fazendo insert
errorLevel = str(mae)
#dataModeling = map(lambda e: (dateTimeObj, e, errorLevel), previsoes2)
dataModeling = list(zip(previsoes2, historyoriginal, datecollect, servers))

# CRIANDO CONEXAO NO PSQL                                                                                                                                                                                           
conn = psycopg2.connect(host="192.168.1.250", dbname='networkneural', user='postgres', password='postgres')
cur = conn.cursor()

for prev, ori, collect, srv in dataModeling:
    cur.execute("INSERT into forecastmemoryconsumption (date, forecastvalue, originalValue, datecollect, hostname, levelerror) VALUES (current_timestamp, '{}', '{}', '{}', '{}', '{}')".format(prev, ori, collect, srv, errorLevel))
    conn.commit()

cur.close()
conn.close()
