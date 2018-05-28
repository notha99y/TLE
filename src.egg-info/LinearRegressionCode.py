'''
Linear Regression code using the numpy package
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tle import *


def error(X, Y, m, b):
    N = len(X)
    sqError = (Y - (m*X + b))**2
    return 1/N * sqError.sum()


def gradDescent(X, Y, m, b, etam=10e-6, etab=10e-3):
    def dm(X, Y, m, b):
        _ = -X*(Y-(m*X + b))
        return _.sum() * 2/len(X)

    def db(X, Y, m, b):
        _ = -(Y - (m*X+b))
        return _.sum()*2/len(X)

    bNew = b - etab * db(X, Y, m, b)
    mNew = m - etam * dm(X, Y, m, b)
    return mNew, bNew


def LinearReg(X, Y, m, b, epoch=101, etam=10e-6, etab=10e-3):
    '''
    Inputs:
    X: input vector
    Y: target vector
    m: gradient
    b: bias

    eta m: learning rate for gradient
    eta b: learning rate for bias

    Output:
    returns a trained m and b

    Description:
    Runs a simple gradient descent algorithm
    '''
    print('Training Linear Regression model...')
    for i in range(epoch):
        err = error(X, Y, m, b)
        m, b = gradDescent(X, Y, m, b, etam, etab)
        if i % (epoch-1)/100 == 0:
            print("Epoch: ", i, "Error: ", err, "New m: ", m, "New b: ", b)
    return m, b


def main(fileName, plotData=True, plotLine=True, plotErr=True, plotGrowth=True):
    numIter = int(10e3)
    data = readTLE(fileName)

    dataY = []
    dataEpoch = []
    listm = []
    listb = []
    for i in range(len(data)):
        dataY.append(data[i].get('Mean Motion'))
        tempEpoch = (data[i].get('Epoch Year') - 16.0)*365 + data[i].get('Epoch')
        dataEpoch.append(tempEpoch)
    dataEpoch = np.array(dataEpoch)
    dataY = np.array(dataY)

    m = 0  # initial
    b = 0  # initial

    listm.append(m)
    listb.append(b)
    if plotData:
        plt.title("Mean Motion Scatter plot against Epoch")
        plt.scatter(dataEpoch, dataY, s=100, alpha=0.5)
        plt.show()

    listErr = []
    print("Commencing Training...")
    for i in range(numIter):
        err = error(dataEpoch, dataY, m, b)
        listErr.append(err)
        m, b = gradDescent(dataEpoch, dataY, m, b)
        listm.append(m)
        listb.append(b)
        if i % 1000 == 0:
            print("Epoch: ", i, "Error: ", err, "New m: ", m, "New b: ", b)

    if plotLine:
        xline = np.linspace(0, dataEpoch[-1], len(dataEpoch))
        yline = xline * m + b
        plt.title("Mean Motion Scatter plot against Epoch with trained LR line")
        plt.scatter(dataEpoch, dataY, s=100, alpha=0.5)
        plt.plot(xline, yline, c='r')
        plt.show()

    if plotErr:
        plt.plot(listErr)
        plt.show()

    if plotGrowth:
        for i in range(len(listm)):
            if i % 1000 == 0:
                yline = xline * listm[i] + listb[i]
                plt.title("Learning of LR. Eproch = {}".format(i))
                plt.plot(xline, yline, c='k', label='Epoch' + repr(i))
                plt.scatter(dataEpoch, dataY, s=100, alpha=0.5)
                # plt.legend()
                axes = plt.gca()
                # axes.set_xlim([0.01,0.1])
                # axes.set_ylim([13,17])
                plt.show()


if __name__ == '__main__':
    main('sat41167.txt')
