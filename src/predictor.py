'''
This script does the prediction of the future Two Line Elements (TLE) given a certain Satellite's TLE
'''

import numpy as np
import matplotlib.pyplot as plt
from tle import *
from LinearRegressionCode import *


def predictTLELinearReg(data, plotLines=True, getStats=True):
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

    dataBStar = np.array(dataBStar)
    dataIncl = np.array(dataIncl)
    dataRAAN = np.array(dataRAAN)
    dataEccentricity = np.array(dataEccentricity)
    dataAOP = np.array(dataAOP)
    dataMeanMotion = np.array(dataMeanMotion)
    dataMeanAnomaly = np.array(dataMeanAnomaly)
    dataEpoch = np.array(dataEpoch)
    print('============================================================')
    print('dataEpoch is : --------------', dataEpoch[68:73])
    print('============================================================')
    xline = np.linspace(0, dataEpoch[-1], len(dataEpoch))

    mBStar, bBStar = LinearReg(dataEpoch, dataBStar, 0, 0, 10001, 10e-6, 10e-3)
    predBStar = xline*mBStar + bBStar
    mIncl, bIncl = LinearReg(dataEpoch, dataIncl, 0, 0, 10001, 10e-6, 10e-3)
    predIncl = xline*mIncl + bIncl
    mEcc, bEcc = LinearReg(dataEpoch, dataEccentricity, 0, 0, 1001, 10e-6, 10e-3)
    predEccentricity = mEcc*xline + bEcc
    mMeanMotion, bMeanMotion = LinearReg(dataEpoch, dataMeanMotion, 0, 0, 10001, 10e-6, 10e-3)
    predMeanMotion = xline*mMeanMotion + bMeanMotion

    # Unwrapping the angular quantitites
    dataAOPUnwrapped = unwrapping(dataAOP)
    dataRAANUnwrapped = unwrapping(dataRAAN, False)
    dataMeanAnomalyUnwrapped = unwrapping(dataMeanAnomaly, False)

    print('Predicting for the unrwapped values....')
    mAOPUnwrapped, bAOPUnwrapped = LinearReg(dataEpoch, dataAOPUnwrapped, 0, 0, 10001, 10e-6, 10e-3)
    predAOPUnwrapped = xline*mAOPUnwrapped + bAOPUnwrapped
    mRAANUnwrapped, bRAANUnwrapped = LinearReg(
        dataEpoch, dataRAANUnwrapped, 0, 0, 10001, 10e-6, 10e-3)
    predRAANUnwrapped = xline*mRAANUnwrapped + bRAANUnwrapped
    mMeanAnomalyUnwrapped, bMeanAnomalyUnwrapped = LinearReg(
        dataEpoch, dataMeanAnomalyUnwrapped, 0, 0, 10001, 10e-6, 10e-3)
    predMeanAnomalyUnwrapped = xline*mMeanAnomalyUnwrapped + bMeanAnomalyUnwrapped

    if getStats:
        print('Getting the approximate rate of change of data... dy/dx approx (y2-y1)/(x2-x1)')
        statsFile = open('StatsSheet.txt', 'w')
        ROCdataBStar = rateofchange(dataEpoch, dataBStar)  # ROC is rate of change
        BStarMean, BStarStdev = returnMeanNStd(ROCdataBStar)
        InclMean, InclStdev = returnMeanNStd(dataIncl)
        EccentricityMean, EccentricityStdev = returnMeanNStd(dataEccentricity)
        AOPMean, AOPStdev = returnMeanNStd(dataAOPUnwrapped)
        RAANMean, RAANStdev = returnMeanNStd(dataRAANUnwrapped)
        MeanAnomalyMean, MeanAnomalyStdev = returnMeanNStd(dataMeanAnomalyUnwrapped)

        statsFile.write('BStar has a measurement mean of ' + repr(BStarMean) +
                        ' and stdev of ' + repr(BStarStdev) + '\n')
        statsFile.write('Inclination has a measurement mean of ' +
                        repr(InclMean) + ' and stdev of ' + repr(InclStdev) + '\n')
        statsFile.write('Eccentricity has a measurement mean of ' +
                        repr(EccentricityMean) + ' and stdev of ' + repr(EccentricityStdev) + '\n')
        statsFile.write('Arguement of Perigee has a measurement mean of ' +
                        repr(AOPMean) + ' and stdev of ' + repr(AOPStdev) + '\n')
        statsFile.write('RAAN has a measurement mean of ' + repr(RAANMean) +
                        ' and stdev of ' + repr(RAANStdev) + '\n')
        statsFile.write('Mean Anomaly has a measurement mean of ' +
                        repr(MeanAnomalyMean) + ' and stdev of ' + repr(MeanAnomalyStdev) + '\n')

        statsFile.close()
    if plotLines:
        fig, ax = plt.subplots(3, 2, sharex='all')
        ax[0][0].plot(xline, predBStar, c='r')
        ax[0][0].scatter(dataEpoch, dataBStar, s=100, alpha=0.5)
        ax[0][0].set_title('BStar Predictor')

        ax[0][1].plot(xline, predIncl, c='r')
        ax[0][1].scatter(dataEpoch, dataIncl, s=100, alpha=0.5)
        ax[0][1].set_title('Inclination Predictor')

        ax[1][0].plot(xline, predEccentricity, c='r')
        ax[1][0].scatter(dataEpoch, dataEccentricity, s=100, alpha=0.5)
        ax[1][0].set_title('Eccentricity Predictor')

        ax[1][1].plot(xline, predAOPUnwrapped, c='r')
        ax[1][1].scatter(dataEpoch, dataAOPUnwrapped, s=100, alpha=0.5)
        ax[1][1].set_title('Arguement of Pregiee Unwrapped Predictor')

        ax[2][0].plot(xline, predRAANUnwrapped, c='r')
        ax[2][0].scatter(dataEpoch, dataRAANUnwrapped, s=100, alpha=0.5)
        ax[2][0].set_title('RAAN Unwrapped Predictor')

        ax[2][1].plot(xline, predMeanAnomalyUnwrapped, c='r')
        ax[2][1].scatter(dataEpoch, dataMeanAnomalyUnwrapped, s=100, alpha=0.5)
        ax[2][1].set_title('Mean Anomaly Unwrapped Predictor')

        plt.show()

    return mBStar, bBStar, mIncl, bIncl, mEcc, bEcc, mMeanMotion, bMeanMotion, mAOPUnwrapped, bAOPUnwrapped, mRAANUnwrapped, bRAANUnwrapped, mMeanAnomalyUnwrapped, bMeanAnomalyUnwrapped


def main(fileName, testFileName):
    data = readTLE(fileName)
    mBStar, bBStar, mIncl, bIncl, mEcc, bEcc, mMeanMotion, bMeanMotion, mAOPUnwrapped, bAOPUnwrapped, mRAANUnwrapped, bRAANUnwrapped, mMeanAnomalyUnwrapped, bMeanAnomalyUnwrapped = predictTLELinearReg(
        data)
    testData = readTLE(testFileName)

    xline = np.linspace(0, 700, 10e4)

    print('Generating Linear Regression Model...')
    predBStar = xline*mBStar + bBStar
    predIncl = xline*mIncl + bIncl
    predEccentricity = mEcc*xline + bEcc
    predMeanMotion = xline*mMeanMotion + bMeanMotion
    predAOPUnwrapped = xline*mAOPUnwrapped + bAOPUnwrapped
    predRAANUnwrapped = xline*mRAANUnwrapped + bRAANUnwrapped
    predMeanAnomalyUnwrapped = xline*mMeanAnomalyUnwrapped + bMeanAnomalyUnwrapped

    predAOP = wrapping(predAOPUnwrapped)
    predRAAN = wrapping(predRAANUnwrapped, False)
    predMeanAnomaly = wrapping(predMeanAnomalyUnwrapped, False)

    print('Extracting attributes from testTLE...')
    testDataEpoch = []
    testDataBStar = []
    testDataIncl = []
    testDataRAAN = []
    testDataEccentricity = []
    testDataAOP = []
    testDataMeanAnomaly = []
    testDataMeanMotion = []
    testDataFirstDMeanMotion = []
    testDataSecondDMeanMotion = []

    for i in range(len(testData)):
        testDataBStar.append(testData[i].get('BStar'))
        testDataIncl.append(testData[i].get('Incl'))
        testDataRAAN.append(testData[i].get('RAAN'))
        testDataEccentricity.append(testData[i].get('Eccentricity'))
        testDataAOP.append(testData[i].get('AOP'))
        testDataMeanMotion.append(testData[i].get('Mean Motion'))
        testDataMeanAnomaly.append(testData[i].get('Mean Anomaly'))
        testDataFirstDMeanMotion.append(testData[i].get('1st dmdt/2'))
        testDataSecondDMeanMotion.append(testData[i].get('2nd dmdt/2'))
        tempEpoch = (testData[i].get('Epoch Year') - 16.0)*365 + testData[i].get('Epoch')
        testDataEpoch.append(tempEpoch)

    fig, ax = plt.subplots(3, 2, sharex='all')

    ax[0][0].scatter(xline, predBStar, c='r', marker=".", alpha=0.5)
    ax[0][0].scatter(testDataEpoch, testDataBStar, s=100, alpha=0.5)
    ax[0][0].set_title('BStar Predictor')

    ax[0][1].scatter(xline, predIncl, c='r', marker=".", alpha=0.5)
    ax[0][1].scatter(testDataEpoch, testDataIncl, s=100, alpha=0.5)
    ax[0][1].set_title('Inclination Predictor')

    ax[1][0].scatter(xline, predEccentricity, c='r', marker=".", alpha=0.5)
    ax[1][0].scatter(testDataEpoch, testDataEccentricity, s=100, alpha=0.5)
    ax[1][0].set_title('Eccentricity Predictor')

    ax[1][1].scatter(xline, predAOP, c='r', marker=".", alpha=0.5)
    ax[1][1].scatter(testDataEpoch, testDataAOP, s=100, alpha=0.5)
    ax[1][1].set_title('Arguement of Pregiee Predictor')

    ax[2][0].scatter(xline, predRAAN, c='r', marker=".", alpha=0.5)
    ax[2][0].scatter(testDataEpoch, testDataRAAN, s=100, alpha=0.5)
    ax[2][0].set_title('RAAN Predictor')

    ax[2][1].scatter(xline, predMeanAnomaly, c='r', marker=".", alpha=0.5)
    ax[2][1].scatter(testDataEpoch, testDataMeanAnomaly, s=100, alpha=0.5)
    ax[2][1].set_title('Mean Anomaly Predictor')
    plt.show()


if __name__ == '__main__':
    main('sat41169.txt', 'sat41169test27junto7jul.txt')
