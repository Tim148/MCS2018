import numpy as np
import math
import matplotlib.pyplot as plt
import random as rnd

def createNet(Net, step, deg):
    probs = deg[0:step]/(2*(step-1))
    ind = np.random.choice(np.arange(0,step,1), size=1, p=probs)

    Net[step, ind] = 1
    Net[ind, step] = 1

    return Net


def pref_at():
    NN = 5000


    Net = np.zeros((NN, NN))

    Net[0,1] = 1
    Net[1,0] = 1

    outDeg = np.sum(Net, axis=1)

    for tt in range(NN-2):
        Net = createNet(Net, tt+2, outDeg)
        outDeg = np.sum(Net, axis=1)

    outUniques, outCounts = np.unique(outDeg, return_counts=True)

    avgDeg = np.average(outDeg)

    lu = np.log(outUniques)
    lc = np.log(outCounts)

    print('Average Degree of Network: %f' %avgDeg)

    plt.scatter(outUniques, outCounts, marker='.')
    plt.xlabel('ln(Degree of Network)')
    plt.ylabel('ln(Number of Nodes with Degree x)')

    plt.show()




pref_at()
