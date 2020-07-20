#!/usr/bin/env python
# coding: utf-8

# # Previsão de picos de CPU

# ### Carregando bibliotecas:

import warnings
warnings.filterwarnings("ignore")
import operator
import statistics
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.initializers import VarianceScaling
from keras.regularizers import l2
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import StratifiedKFold

# ### Selecionando dados:

data = pd.read_csv('C:\\Users\\LuisHenriqueVinhali\\Desktop\\classification\\data\\cpu.csv')

print(data)

# ### Funções de modelamento:

# #### Entrada da camada:
# 
# >m1 = Média de 12 leituras (Em uma janela de 60 dados) - Exemplo ((2 + 5 + 7 ...) / 12
# 
# >d1 = desvio padrão dos 12 dados
# 
# E assim sucessivamente até formar m5, d5 (12x5 = 60)
# 
# #### Saída da camada:
# 
# >0-20 = Quantas vezes os valores são repetidos no intervalo de 0 a 20 nas próximas 30 leituras (Linha 61,62,62 ...)
# 
# E assim sucessivamente até formar 20-40.40-60.60-80.80-100
# 
# #### Transformando em 0 e 1
# 
# Em seguida é selecionado a maior ocorrência de cada coluna e dividido todos os valores da respectiva coluna pela maior ocorrência, exemplo:
# 
# >m1 = (Xn > Xn) / Xn

def histogramNeuronsInput(result):
    """ Generates histogram of input neurons """
    
    fig, ax = plt.subplots(figsize=(8,4))
    for i in range(len(result)):
        data = np.array(result[i])
        x=np.arange(len(data)) + i*6
        # draw averages
        ax.bar(x-0.2, data[:,0], color='C0', width=0.4)
        # draw std
        ax.bar(x+0.2, data[:,1], color='C1', width=0.4)
    # turn off xticks
    ax.set_xticks([])
    ax.legend(labels=['Average', 'Standard deviation'])
    leg = ax.get_legend()
    leg.legendHandles[0].set_color('C0')
    leg.legendHandles[1].set_color('C1')
    plt.ylabel('Consume')
    plt.xlabel('Number of elements (Every 5 is a new block)')

    return plt.show()

def histogramNeuronsOutput(result):
    """ Generates histogram of output neurons """
    
    colors = ['blue', 'green', 'yellow', 'orange', 'red']
    labels = ['0-20', '20-40', '40-60', '60-80', '80-100']
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, data in enumerate(result):
        x = np.arange(len(data)) + i*6
        bars = ax.bar(x, data, color=colors, width=0.4)
        if i == 0:
            for bar, label in zip(bars, labels):
                bar.set_label(label)
    ax.set_xticks([])
    ax.legend()
    ax.set_title("Histogram")
    ax.set_ylabel('Consume')
    ax.set_xlabel('Percent')
    
    return plt.show()

def standardDeviation(data):
    """ Calculates standard deviation """
    
    return statistics.stdev(data)
       
def average(data):
    """ Calculates average """
    
    return statistics.mean(data)

def captureOcurrences(elements, n):
    """ Capture an X number of elements within a list """
    
    return [elements[i: i+n] for i in range(0, len(elements), n)]

def neuronsInput(elements):
    """ Generates input neuron modeling (5 averages, 5 standard deviations - Between 12 occurrences in a window of 60 readings) """
    
    result = []
    temp = []
    start = 0
    limit = 60
    size = int(len(elements))
    TargetDivision = int(size / 30)
    repetitions = 0
    five = 0

    while repetitions < TargetDivision:
        temp = []

        five += 1
        ocurrences = captureOcurrences(elements[start: limit],12)
        for i in ocurrences:
            m = average(i)
            sd = standardDeviation(i)
            temp.append([m,sd])

        result.append(temp)

        repetitions += 1
        limit += 10
        start += 10

    return result

def neuronsOutput(elements):
    """ Generates output neuron modeling (Histogram of the next 30 data readings) """
    
    result = []
    start = 61
    limit = 90
    size = int(len(elements))
    TargetDivision = int(size / 30)
    repetitions = 0

    while repetitions < TargetDivision:

        counter=collections.Counter(elements[start: limit])
        
        consumption0_20 = 0
        consumption20_40 = 0
        consumption40_60 = 0
        consumption60_80 = 0
        consumption80_100 = 0
        for key in counter:
            if key <= 20:
                consumption0_20 += int(counter[key])
            elif key > 20 and key < 40:
                consumption20_40 += int(counter[key])
            elif key > 40 and key < 60:
                consumption40_60 += int(counter[key])
            elif key > 60 and key < 80:
                consumption60_80 += int(counter[key])
            elif key > 80 and key < 100:
                consumption80_100 += int(counter[key])

        result.append([consumption0_20,consumption20_40,consumption40_60,consumption60_80,consumption80_100])

        repetitions += 1
        limit += 10
        start += 10

    return result

def binaryInput(data):
    """ I divided the values ​​of each column by the highest occurrence in the column """
    
    max_average = 0
    max_deviation = 0
    for j in range(len(data[0])):
        for i in range(len(data)):
            if data[i][j][0] > max_average:
                max_average = data[i][j][0]
            if data[i][j][1] > max_deviation:
                max_deviation = data[i][j][1]
        for p in range(len(data)):
            if max_average != 0:
                data[p][j][0] = round(data[p][j][0] / max_average, 3)
            if max_deviation != 0:
                data[p][j][1]  = round(data[p][j][1] / max_deviation, 3)
        max_average = 0
        max_deviation = 0
        
    return data

def binaryOutput(data):
    """ I divided the values ​​of each column by the highest occurrence in the column """
    
    max_consume = 0
    reverse = []
    for j in range(len(data[0])):
        for i in range(len(data)):
            if data[i][j] > max_consume:
                max_consume = data[i][j]
        for p in range(len(data)):
            if max_consume != 0:
                data[p][j] = round(data[p][j] / max_consume, 3)

            reverse.append(max_consume)
        max_consume = 0
        
    return data, reverse

def conversionDataframe(dataNeuronInput,dataNeuronOutput):
    """ Converts data to a dataframe pandas """
    
    ni = pd.DataFrame(data= dataNeuronInput)
    ni.columns = ['m1,d1', 'm2,d2', 'm3,d3', 'm4,d4', 'm5,d5']
    no = pd.DataFrame(data= dataNeuronOutput)
    no.columns = ['0-20', '20-40', '40-60', '60-80', '80-100']

    return pd.concat([ni, no], axis=1)

def modeling(data):
    """ Generates the initial model for training the neural network """
    
    readings = data.iloc[:, 1].values
    dataNeuronInput = neuronsInput(readings)
    dataNeuronOutput = neuronsOutput(readings)
    dataFrameNoBinary = conversionDataframe(dataNeuronInput, dataNeuronOutput)
    binaryNeuronInput = binaryInput(dataNeuronInput)
    binaryNeuronOutput, reverseNeuronOutput = binaryOutput(dataNeuronOutput)
    dataFrameBinary = conversionDataframe(binaryNeuronInput, binaryNeuronOutput)

    return dataFrameBinary, np.asarray(captureOcurrences(reverseNeuronOutput,5), dtype=np.float32)


# ### Histograma: Médias versus Desvio padrão

# *Antes da divisão pela maior ocorrência de cada critério*

readings = data.iloc[:, 1].values
dataNeuronInput = neuronsInput(readings)
histogramNeuronsInput(dataNeuronInput)


# ### Transformando X e Y em uma matriz 1D

df, reverse = modeling(data)

X = np.array(df['m1,d1'].values.tolist())
X = np.append(X, np.array(df['m2,d2'].values.tolist()), axis = 1)
X = np.append(X, np.array(df['m3,d3'].values.tolist()), axis = 1)
X = np.append(X, np.array(df['m4,d4'].values.tolist()), axis = 1)
X = np.append(X, np.array(df['m5,d5'].values.tolist()), axis = 1)

Y = []
Y.append(np.asarray(df['0-20'], dtype=np.float32))
Y.append(np.asarray(df['20-40'], dtype=np.float32))
Y.append(np.asarray(df['40-60'], dtype=np.float32))
Y.append(np.asarray(df['60-80'], dtype=np.float32))
Y.append(np.asarray(df['80-100'], dtype=np.float32))
Y = np.transpose(np.asarray(Y))


# ### Visualizando X:

print(pd.DataFrame(np.array(X)))


# ### Visualizando Y:

print(pd.DataFrame(np.array(Y)))

# Shapes

print(X.shape)
print(Y.shape)

# ### Definindo 5 folds para validação

kfold = StratifiedKFold(n_splits=5, shuffle=True)
cvscores = []


# ### Modelo de aprendizado profundo:

# *Descrição do modelo*
# 
# >kernel_regularizer = Regularizador de peso da camada
# 
# >kernel_initializer = Inicialização da camada
# 
# >model.compile = Compilamento do modelo 
# 
# >model.fit = Treinamento do modelo
# 
# >model.evaluate = Avaliação do modelo

# ### Criando um novo objeto com idxmax(axis=1) para encontrar o alvo com maior probabilidade em Y

pd.DataFrame(Y).idxmax(axis=1)
print(pd.DataFrame(Y).idxmax(axis=1).shape)

for train, test in kfold.split(X, pd.DataFrame(Y).idxmax(axis=1)):
    model = Sequential()
    model.add(Dense(10,
                kernel_regularizer=l2(0.001),
                kernel_initializer=VarianceScaling(), 
                activation='sigmoid'))
    model.add(Dense(5, 
                kernel_regularizer=l2(0.01),
                kernel_initializer=VarianceScaling(),                 
                activation='sigmoid'))
    
    model.compile(loss='mse', optimizer='adam', metrics=['acc'])
    
    model.fit(X[train], Y[train], epochs=50, batch_size=5, verbose = 0,
              validation_data=(X[test], Y[test]))

    scores = model.evaluate(X[test], Y[test], verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    cvscores.append(scores[1] * 100)


print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))


print(model.summary())


y = model.predict(pd.DataFrame(np.array(X)))

multiple = []
for i,j in zip(y,reverse):
    multiple.append([i[0] * j[0], i[1] * j[1], i[2] * j[2], i[3] * j[3],  i[4] * j[4]])
    
result = pd.DataFrame(np.array(multiple))
print(result)