# -*- coding: utf-8 -*-
import operator
import statistics
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def histogramInput(result):
    fig, ax = plt.subplots(figsize=(10,6))
    for i in range(len(result)):
        data = np.array(result[i])
        x=np.arange(len(data)) + i*6
        # draw means
        ax.bar(x-0.2, data[:,0], color='C0', width=0.4)
        # draw std
        ax.bar(x+0.2, data[:,1], color='C1', width=0.4)
    # separation line
    ax.axvline(4.75)
    # turn off xticks
    ax.set_xticks([])
    ax.legend(labels=['Mean', 'Standard deviation'])
    leg = ax.get_legend()
    leg.legendHandles[0].set_color('C0')
    leg.legendHandles[1].set_color('C1')
    plt.title("Histogram: Mean versus Standard Deviation")
    plt.ylabel('Consume')
    plt.xlabel('Number of elements (Every 5 is a new block)')

    return plt.show()

def histogramOutput(result):
    colors = ['blue', 'green', 'yellow', 'orange', 'red']
    labels = ['0-20', '20-40', '40-60', '60-80', '80-100']
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, data in enumerate(result):
        x = np.arange(len(data)) + i*6
        bars = ax.bar(x, data, color=colors, width=0.4)
        if i == 0:
            for bar, label in zip(bars, labels):
                bar.set_label(label)
        if i < len(result) - 1:
            # separation line after each part, but not after the last
            ax.axvline(4.75 + i*6, color='black', linestyle=':')
    ax.set_xticks([])
    ax.legend()
    ax.set_title("Histogram")
    ax.set_ylabel('Consume')
    ax.set_xlabel('Percent')
    plt.show()

def standardDeviation(data):
    return statistics.stdev(data)
       
def mean(data):
    return statistics.mean(data)

def captureOcurrences(elements, n):
    L = len(elements)
    return [elements[i: i+n] for i in range(0, L, n)]

def input(elements):

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
            print("[INFO] 12 Ocurrences: {}".format(i))
            print("[INFO] Mean: {}".format(mean(i)))
            m = mean(i)
            print("[INFO] Standard Deviation: {}".format(standardDeviation(i)))
            sd = standardDeviation(i)
            print("Result: [{},{}]\n\n".format(m,sd))
            temp.append([m,sd])

        print("[INFO] Result Cycle {}: \n{}\n\n".format(repetitions+1,result))
        result.append(temp)

        repetitions += 1
        limit += 10
        start += 10

    histogramInput(result)
    return result

def output(elements):

    result = []
    start = 61
    limit = 90
    size = int(len(elements))
    TargetDivision = int(size / 30)
    repetitions = 0

    while repetitions < TargetDivision:

        print("[INFO] Reading [{}:{}]".format(start, limit))
        print("[INFO] Elements:\n{}".format(elements[start: limit]))
        counter=collections.Counter(elements[start: limit])
        bar = 0
        bar1 = 0
        bar2 = 0
        bar3 = 0
        bar4 = 0
        for key in counter:
            if key <= 20:
                bar += int(counter[key])
            elif key > 20 and key < 40:
                bar1 += int(counter[key])
            elif key > 40 and key < 60:
                bar2 += int(counter[key])
            elif key > 60 and key < 80:
                bar3 += int(counter[key])
            elif key > 80 and key < 100:
                bar4 += int(counter[key])

        print("[INFO] Histogram: 0-20 [{}], 20-40 [{}], 40-60 [{}], 60-80 [{}], 80-100 [{}]\n\n".format(bar,bar1,bar2,bar3,bar4))

        result.append([bar,bar1,bar2,bar3,bar4])

        repetitions += 1
        limit += 10
        start += 10
    
    histogramOutput(result)
    return result

def divisonBigger(data):
    max_month = 0
    max_day = 0
    for j in range(len(data[0])):
        for i in range(len(data)):
            if data[i][j][0] > max_month:
                max_month = data[i][j][0]
            if data[i][j][1] > max_day:
                max_day = data[i][j][1]
        for p in range(len(data)):
            if max_month != 0:
                data[p][j][0] = round(data[p][j][0] / max_month, 3)
            if max_day != 0:
                data[p][j][1]  = round(data[p][j][1] / max_day, 3)
        max_month = 0
        max_day = 0
    return data

def conversionDataframe(NeuronInputNeuronInputay,NeuronOutput):
    
    print("[INFO] Converting for dataframe")
    ni = pd.DataFrame(data= NeuronInputNeuronInputay)
    ni.columns = ['m1,d1', 'm2,d2', 'm3,d3', 'm4,d4', 'm5,d5']

    no = pd.DataFrame(data= NeuronOutput)
    no.columns = ['0-20', '20-40', '40-60', '60-80', '80-100']

    return pd.concat([ni, no], axis=1)

data = pd.read_csv('/home/vinhali/Desktop/classification/data/minute.csv')
Y = data.iloc[:, 1].values
NeuronInputNeuronInputay = input(Y)
NeuronOutput = output(Y)

a = divisonBigger(NeuronInputNeuronInputay)
#b = divisonBigger(NeuronOutput)
print(conversionDataframe(a, NeuronOutput))
