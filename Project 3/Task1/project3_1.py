import numpy as np
import math
import matplotlib.pyplot as plt

def createNet(NN, lDens):
    Net = np.random.choice([0,1], size=([NN,NN]), p=[(1-lDens), lDens])

    return Net


def task_one(NN, lDens):

    Net = createNet(NN, lDens)

    # calculate degree distributions
    # in degree
    inDeg = np.sum(Net, axis=0)
    outDeg = np.sum(Net, axis=1)
    inUniques, inCounts = np.unique(inDeg, return_counts=True)
    outUniques, outCounts = np.unique(outDeg, return_counts=True)

    avgDeg = np.average(inDeg)
    avgDeg1 = np.average(outDeg)

    if avgDeg !=avgDeg1:
        print('Error, Average of In- and Out-Degree not equal!')
        exit()

    print('Average Degree of Network: %f' %avgDeg)

    plt.scatter(inUniques, inCounts, marker='.')
    plt.scatter(outUniques, outCounts, marker='x')
    plt.xlabel('Degree of Network')
    plt.ylabel('Number of Nodes with Degree x')

    plt.show()



NN = 5000
lDens = 0.0016

task_one(NN, lDens)
