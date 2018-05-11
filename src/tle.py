'''
This script contains the helper functions to read and plot Two Line Element (TLE) files
You can also run the script to do plots of the TLE
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def readTLE(tle):
    '''
    First Line
    Epoch Year (19-20)
    Epoch (21-32)
    First time derivative of the mean motion divided by 2 (32-43)
    Second time derivative of mean motion divided by 6 (45-52)
    BStar drag term (54-61)

    Second Line
    Inclination (degrees) (09-16)
    RAAN (degrees) (18-25)
    Eccentricity (27-33)
    Argument of perigee (35-42)
    Mean Anomaly (44-51)
    Mean Motion (53-63)
    Rev number at epoch (64-68)
    '''
    temp = []
    df = pd.read_csv(tle, header=None).as_matrix()
    for i in range(df.shape[0]):
        if i % 2 == 0:
            test_df1 = df[i, 0]
            test_df2 = df[i+1, 0]

            dic1 = {'Epoch Year': float(test_df1[18:20])}
            dic2 = {'Epoch': float(test_df1[20:32])}
            dic3 = {'1st dmdt/2': float(test_df1[32:43])}
            dic4 = {'2nd dmdt/2': float(test_df1[44:50]) * 10**(-float(test_df1[51]))}
            dic5 = {'BStar': float(test_df1[53:59]) * 10**(-float(test_df1[60]))}
            dic6 = {'Incl': float(test_df2[8:16])}
            dic7 = {'RAAN': float(test_df2[17:25])}
            dic8 = {'Eccentricity': float('.' + test_df2[26:33])}
            dic9 = {'AOP': float(test_df2[34:42])}
            dic10 = {'Mean Anomaly': float(test_df2[43:51])}
            dic11 = {'Mean Motion': float(test_df2[52:63])}
            dic12 = {'Rev Number': float(test_df2[63:68])}

            temp.append({**dic1, **dic2, **dic3, **dic4, **dic5, **dic6, **
                         dic7, **dic8, **dic9, **dic10, **dic11, **dic12})

    return temp


def returnMeanNStd(data):
    return data.mean(), data.std()


def rateofchange(X, Y):
    rateofchange = []
    for i in range(0, len(X)-1):
        if X[i+1] == X[i]:
            print(i)
        # print('i: ', i, 'dX: ', X[i+1] - X[i])
        d = (Y[i + 1] - Y[i])/(X[i + 1] - X[i])
        rateofchange.append(d)
    return np.array(rateofchange)


def unwrapping(data, increasing=True):
    counter = 0
    dataUnwrapped = []
    thresholdDe = 200
    thresholdIn = 100
    if increasing:
        # print("The unwrapping data is increasing with Epoch")
        for i in range(len(data)):
            dataUnwrapped.append(data[i] + counter*360.0)
            if i < len(data)-1 and data[i+1] - data[i] < -thresholdIn:
                # print('taking a step upwards of 360 deg: ', i)
                counter += 1
    else:
        # print("The unwrapping data is decreasing with Epoch")
        for i in range(len(data)):
            dataUnwrapped.append(data[i] + counter*360.0)
            if i < len(data)-1 and data[i+1] - data[i] > thresholdDe:
                # print('taking a step downwards of 360 deg: ', i)
                counter -= 1
    return np.array(dataUnwrapped)


def wrapping(data, increasing=True):
    counter = 0
    dataWrapped = []
    if increasing:
        # print("Wrapping an increasing data")
        for i in range(len(data)):
            dataWrapped.append(data[i] + counter*360.0)
            if data[i] + counter*360.0 > 360.0:
                counter -= 1
    else:
        # print("Wrapping a decreasing data")
        for i in range(len(data)):
            dataWrapped.append(data[i] + counter*360.0)
            if data[i] + counter*360.0 < 0:
                counter += 1
    return np.array(dataWrapped)


def plotTLE(fileName, plot=True, angleUnwrapped=True):
    plt.rcParams['figure.figsize'] = [20, 10]  # Setting the figure size
    data = readTLE(fileName)

    name = fileName.split('.txt')[0][-8:]

    dataEpoch = []
    dataBStar = []
    dataIncl = []
    dataRAAN = []
    dataEccentricity = []
    dataAOP = []
    dataMeanAnomaly = []
    dataMeanMotion = []
    dataFirstDMeanMotion = []
    dataSecondDMeanMotion = []

    for i in range(len(data)):
        dataBStar.append(data[i].get('BStar'))
        dataIncl.append(data[i].get('Incl'))
        dataRAAN.append(data[i].get('RAAN'))
        dataEccentricity.append(data[i].get('Eccentricity'))
        dataAOP.append(data[i].get('AOP'))
        dataMeanMotion.append(data[i].get('Mean Motion'))
        dataMeanAnomaly.append(data[i].get('Mean Anomaly'))
        dataFirstDMeanMotion.append(data[i].get('1st dmdt/2'))
        dataSecondDMeanMotion.append(data[i].get('2nd dmdt/2'))
        tempEpoch = (data[i].get('Epoch Year') - 16.0)*365 + data[i].get('Epoch')
        dataEpoch.append(tempEpoch)
    if plot:
        fig, ax = plt.subplots(3, 3, sharex='all')

        print("Reading the data for " + repr(fileName) + "... Please wait...")
        ax[0][0].scatter(dataEpoch, dataBStar, s=50, alpha=0.5, c='b')
        ax[0][0].set_title('BStar')
        ax[0][1].scatter(dataEpoch, dataIncl, s=50, alpha=0.5, c='r')
        ax[0][1].set_title('Inclination')
        ax[0][2].scatter(dataEpoch, dataRAAN, s=50, alpha=0.5, c='y')
        ax[0][2].set_title('RAAN')
        ax[1][0].scatter(dataEpoch, dataEccentricity, s=50, alpha=0.5, c='g')
        ax[1][0].set_title('Eccentricity')
        ax[1][1].scatter(dataEpoch, dataAOP, s=50, alpha=0.5, c='c')
        ax[1][1].set_title('Argument of Perigee')
        ax[1][2].scatter(dataEpoch, dataMeanAnomaly, s=50, alpha=0.5, c='m')
        ax[1][2].set_title('Mean Anomaly')
        ax[2][0].scatter(dataEpoch, dataMeanMotion, s=50, alpha=0.5, c='k')
        ax[2][0].set_title('Mean Motion')
        ax[2][1].scatter(dataEpoch, dataFirstDMeanMotion, s=50, alpha=0.5, c='k')
        ax[2][1].set_title('First derivative Mean Motion')
        ax[2][2].scatter(dataEpoch, dataSecondDMeanMotion, s=50, alpha=0.5, c='k')
        ax[2][2].set_title('Second derivative Mean Motion')
        ax[0][0].grid(True)
        ax[0][1].grid(True)
        ax[0][2].grid(True)
        ax[1][0].grid(True)
        ax[1][1].grid(True)
        ax[1][2].grid(True)
        ax[2][0].grid(True)
        ax[2][1].grid(True)
        ax[2][2].grid(True)
        fig.suptitle(repr(name))
        plt.show()

    if angleUnwrapped:
        '''
        data that needs to be unwrapped
        1) RAAN 2) AOP 3) Mean Anomaly
        Check the initial plot to see if the data is increasing or decreasing.
        '''

        dataAOPUnwrapped = unwrapping(dataAOP)
        dataRAANUnwrapped = unwrapping(dataRAAN, False)
        dataMeanAnomalyUnwrapped = unwrapping(dataMeanAnomaly, False)

        fig, ax = plt.subplots(3, 3, sharex='all')

        ax[0][0].scatter(dataEpoch, dataBStar, s=50, alpha=0.5, c='b')
        ax[0][0].set_title('BStar')
        ax[0][1].scatter(dataEpoch, dataIncl, s=50, alpha=0.5, c='r')
        ax[0][1].set_title('Inclination')
        ax[0][2].scatter(dataEpoch, dataRAANUnwrapped, s=50, alpha=0.5, c='y')
        ax[0][2].set_title('RAAN Unwrapped')
        ax[1][0].scatter(dataEpoch, dataEccentricity, s=50, alpha=0.5, c='g')
        ax[1][0].set_title('Eccentricity')
        ax[1][1].scatter(dataEpoch, dataAOPUnwrapped, s=50, alpha=0.5, c='c')
        ax[1][1].set_title('Argument of Perigee Unwrapped')
        ax[1][2].scatter(dataEpoch, dataMeanAnomalyUnwrapped, s=50, alpha=0.5, c='m')
        ax[1][2].set_title('Mean Anomaly Unwrapped')
        ax[2][0].scatter(dataEpoch, dataMeanMotion, s=50, alpha=0.5, c='k')
        ax[2][0].set_title('Mean Motion')
        ax[2][1].scatter(dataEpoch, dataFirstDMeanMotion, s=50, alpha=0.5, c='k')
        ax[2][1].set_title('First derivative Mean Motion')
        ax[2][2].scatter(dataEpoch, dataSecondDMeanMotion, s=50, alpha=0.5, c='k')
        ax[2][2].set_title('Second derivative Mean Motion')
        ax[0][0].grid(True)
        ax[0][1].grid(True)
        ax[0][2].grid(True)
        ax[1][0].grid(True)
        ax[1][1].grid(True)
        ax[1][2].grid(True)
        ax[2][0].grid(True)
        ax[2][1].grid(True)
        ax[2][2].grid(True)
        fig.suptitle(repr(fileName) + ' with unwrapped angular attributes')

        plt.show()


def main():
    # plotTLE('sat41167.txt')
    plotTLE('data/sat41169.txt', True, False)
    plotTLE('data/sat39227.txt')
    # plotTLE('landsat7.txt')
    # plotTLE('testT16Jul17.txt')


if __name__ == '__main__':
    main()
