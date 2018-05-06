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

def disease_spread(Net, infected, NN, pp, rr):
    for ii in range(NN):
        if infected[ii] == 1 and rnd.uniform(0,1) < rr:
            infected[ii] = 0
        else:
            true_nn = np.count_nonzero(Net[ii,np.nonzero(infected)])
            if rnd.uniform(0,1) < (1-math.exp(-pp*true_nn)):
                infected[ii] = 1

    return infected


def pref_at():
    nruns = 20
    NN = 5000
    TT = 1001
    pp = np.arange(0.001,0.011,0.001)
    rr = 0.03

    num_inf = np.zeros(TT)
    avg_inf = np.zeros(TT)
    ninfect = 100

    infprob = float(ninfect)/float(NN)
    #infected = np.random.choice([0,1], size=NN, p=[(1-infprob), infprob])
    #num_inf[0] = np.count_nonzero(infected)



    Net = np.zeros((NN, NN))

    Net[0,1] = 1
    Net[1,0] = 1

    outDeg = np.sum(Net, axis=1)

    for tt in range(NN-2):
        Net = createNet(Net, tt+2, outDeg)
        outDeg = np.sum(Net, axis=1)

    for jj in range(pp.size):
        print('p = %f' %pp[jj])
        for ii in range(nruns):
            print('%d. Simulation' %(ii+1))
            infected = np.random.choice([0,1], size=NN, p=[(1-infprob), infprob])
            num_inf[0] = np.count_nonzero(infected)
            for tt in range(TT-1):
                #print('timestep %d' %(tt+1))
                infected = disease_spread(Net, infected, NN, pp[jj], rr)
                num_inf[tt+1] = np.count_nonzero(infected)
            avg_inf = avg_inf + num_inf

        avg_inf = avg_inf / nruns

        plt.plot(avg_inf)

    plt.xlabel('timestep t')
    plt.ylabel('Number of infected individuals')

    plt.show()





pref_at()
