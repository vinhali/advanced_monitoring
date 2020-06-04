# -*- coding: utf-8 -*-
try:
    import operator
    import pandas as pd
    import numpy as np
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt
    import statistics
except ImportError as e:
    print("[FAILED] {}".format(e))

def data():
    data = pd.read_csv('/home/vinhali/Desktop/arima/data/minute.csv')
    X = data.iloc[:, 0].values
    Y = data.iloc[:, 1].values
    return X,Y

def histogram(mean, sd):
    bins = np.linspace(0, 100)
    plt.hist(mean, bins, color='b', alpha=0.5, label='Mean')
    plt.hist(sd, bins, color='r', alpha=0.5, label='Standard Deviation')
    plt.legend(loc="upper right")
    plt.ylabel('Frequency')
    plt.xlabel('Consume')
    plt.title("Histogram: Mean versus Standard Deviation")
    return plt.show()

def standardDeviation(data):
    return statistics.stdev(data)
       
def mean(data):
    return statistics.mean(data)
 
def sampleDivision(elements, n):
    L = len(elements)
    return [elements[i: i+n] for i in range(0, L, n)]

def modeling(elements):
    n = 12
    collections = len(elements)
    L = 60
    sampleShift = []
    sampleShiftMean = []
    sampleShiftStandardDeviation = []
    for i in range(0, L, n):
        j = 0
        while j < collections:
            sampleShiftMean.append(mean(elements[j][i: i+n]))
            sampleShiftStandardDeviation.append(standardDeviation(elements[j][i: i+n]))
            sampleShift.append(mean(elements[j][i: i+n]))
            sampleShift.append(standardDeviation(elements[j][i: i+n]))
            j += 1
    return sampleShift, sampleShiftMean, sampleShiftStandardDeviation

def main():
    try:

        X,Y = data()
        sampleSize = sampleDivision(Y, 60)
        sampleShift, sampleShiftMean, sampleShiftStandardDeviation = modeling(sampleSize)
        sampleRate = sampleDivision(sampleDivision(sampleShift,2), 5)
        print("[INFO] Sample rate generated is:\n\n{}\n\n[END]".format(sampleRate))
        histogram(sampleShiftMean,sampleShiftStandardDeviation)

    except Exception as e:
        print("[FAILED] Caused by: {}".format(e))

if __name__ == "__main__":
    main()
