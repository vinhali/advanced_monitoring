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
    data = pd.read_csv('dir-here/data.csv')
    X = data.iloc[:, 0].values
    Y = data.iloc[:, 1].values
    return X,Y

def histogram(result):
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
        histogram(sampleRate)

    except Exception as e:
        print("[FAILED] Caused by: {}".format(e))

if __name__ == "__main__":
    main()
