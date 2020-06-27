# -*- coding: utf-8 -*-
import operator
import statistics
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def histogramNeuronsInput(result):
    """ Generates histogram of input neurons """
    fig, ax = plt.subplots(figsize=(10,6))
    for i in range(len(result)):
        data = np.array(result[i])
        x=np.arange(len(data)) + i*6
        # draw averages
        ax.bar(x-0.2, data[:,0], color='C0', width=0.4)
        # draw std
        ax.bar(x+0.2, data[:,1], color='C1', width=0.4)
    # separation line
    ax.axvline(4.75)
    # turn off xticks
    ax.set_xticks([])
    ax.legend(labels=['Average', 'Standard deviation'])
    leg = ax.get_legend()
    leg.legendHandles[0].set_color('C0')
    leg.legendHandles[1].set_color('C1')
    plt.title("Histogram: Average versus Standard Deviation")
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
        if i < len(result) - 1:
            # separation line after each part, but not after the last
            ax.axvline(4.75 + i*6, color='black')
    ax.set_xticks([])
    ax.legend()
    ax.set_title("Histogram")
    ax.set_ylabel('Consume')
    ax.set_xlabel('Percent')
    plt.show()

def standardDeviation(data):
    """ Calculates standard deviation """
    return statistics.stdev(data)
       
def average(data):
    """ Calculates average """
    return statistics.mean(data)

def captureOcurrences(elements, n):
    """ Capture an X number of elements within a list """
    L = len(elements)
    return [elements[i: i+n] for i in range(0, L, n)]

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
            print("[INFO] 12 Ocurrences: {}".format(i))
            print("[INFO] Average: {}".format(average(i)))
            m = average(i)
            print("[INFO] Standard Deviation: {}".format(standardDeviation(i)))
            sd = standardDeviation(i)
            print("Result: [{},{}]\n\n".format(m,sd))
            temp.append([m,sd])

        print("[INFO] Cycle Result {}: \n{}\n\n".format(repetitions+1,result))
        result.append(temp)

        repetitions += 1
        limit += 10
        start += 10

    print("[INFO] Final result of phase Neurons Input: \n{}\n".format(result))
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

        print("[INFO] Reading [{}:{}]".format(start, limit))
        print("[INFO] Elements:\n{}".format(elements[start: limit]))
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

        print("[INFO] Histogram: 0-20 [{}], 20-40 [{}], 40-60 [{}], 60-80 [{}], 80-100 [{}]\n\n".format(consumption0_20,consumption20_40,consumption40_60,consumption60_80,consumption80_100))

        result.append([consumption0_20,consumption20_40,consumption40_60,consumption60_80,consumption80_100])

        repetitions += 1
        limit += 10
        start += 10

    print("[INFO] Final result of phase Neurons Output: \n{}\n".format(result))
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
    for j in range(len(data[0])):
        for i in range(len(data)):
            if data[i][j] > max_consume:
                max_consume = data[i][j]
        for p in range(len(data)):
            if max_consume != 0:
                data[p][j] = round(data[p][j] / max_consume, 3)
        max_consume = 0
    return data

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
    histogramNeuronsInput(dataNeuronInput)

    dataNeuronOutput = neuronsOutput(readings)
    histogramNeuronsOutput(dataNeuronOutput)

    dataFrameNoBinary = conversionDataframe(dataNeuronInput, dataNeuronOutput)
    print("[INFO] Viewing non-binary data: \n{}\n\n".format(dataFrameNoBinary))

    binaryNeuronInput = binaryInput(dataNeuronInput)
    binaryNeuronOutput = binaryOutput(dataNeuronOutput)
    dataFrameBinary = conversionDataframe(binaryNeuronInput, binaryNeuronOutput)
    print("[INFO] Converting to binary data frame: \n{}\n\n".format(dataFrameBinary))

    return dataFrameBinary

def main():
    """ Initializes the script """
    print("[INFO] Start *******************************************************************************")
    data = pd.read_csv('/home/vinhali/Desktop/classification/data/minute.csv') # List of data
    modeling(data)
    print("[INFO] End *********************************************************************************")

if __name__ == '__main__':
    main()
