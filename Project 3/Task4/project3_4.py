import numpy as np
import math
import matplotlib.pyplot as plt
import random as rnd
import math

def createNet(Net, step, deg):
    probs = deg[0:step]/(2*(step-1))
    ind = np.random.choice(np.arange(0,step,1), size=1, p=probs)

    Net[step, ind] = 1
    Net[ind, step] = 1

    return Net

def MasterEQ(pi_kmo, nn, kk):
    kk = float(kk)
    top = (nn * (kk - 1.0))
    bot = (2.0 * (nn-2.0) + nn * kk)
    fac = top/bot
    pi_k = pi_kmo * fac



    return pi_k



def pref_at():
    NN = 5000
    nn = 5000.0
    pi = np.zeros(NN+1, dtype=float)
    pi[0] = 0
    pi[1] = (2*(nn-2))/(3*nn - 4)
    print(pi[1])

    for kk in range(NN-1):
        pi[kk+2] = MasterEQ(pi[kk+1], nn, kk+2)

    xval = np.arange(1,100,1)
    print(xval)
    xval = np.log(xval)
    pi = np.log(5000.0 * pi)

    plt.scatter(xval, pi[1:100], marker='.')
    plt.xlabel('ln(Number of Friends)')
    plt.ylabel('ln(Number of individuals with x friends)')

    plt.show()






pref_at()
