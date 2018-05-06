import numpy as np
import math
import matplotlib.pyplot as plt
import random as rnd

def createNet(NN, lDens):
    Net = np.random.choice([0,1], size=([NN,NN]), p=[(1-lDens), lDens])

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




def infection():

    NN = 5000
    lDens = 0.0016
    TT = 1001
    pp = 0.01
    rr = 0.03

    num_inf = np.zeros(TT)
    ninfect = 100
    Net = createNet(NN, lDens)
    infprob = float(ninfect)/float(NN)
    infected = np.random.choice([0,1], size=NN, p=[(1-infprob), infprob])
    num_inf[0] = np.count_nonzero(infected)

    for tt in range(TT-1):
        print('timestep %d' %(tt+1))
        infected = disease_spread(Net, infected, NN, pp, rr)
        num_inf[tt+1] = np.count_nonzero(infected)

    plt.plot(num_inf)
    plt.xlabel('timestep t')
    plt.ylabel('Number of infected individuals')

    plt.show()

def infectprob():
    NN = 5000
    lDens = 0.0016
    TT = 1001
    pp = np.arange(0.001,0.011,0.001)
    rr = 0.03

    num_inf = np.zeros(TT)
    final_num = np.zeros(pp.size)
    ninfect = 100
    Net = createNet(NN, lDens)
    infprob = float(ninfect)/float(NN)
    #infected = np.random.choice([0,1], size=NN, p=[(1-infprob), infprob])
    #num_inf[0] = np.count_nonzero(infected)

    for ii in range(pp.size):
        print('Simulation for p = %f' %pp[ii])
        infected = np.random.choice([0,1], size=NN, p=[(1-infprob), infprob])
        num_inf[0] = np.count_nonzero(infected)
        for tt in range(TT-1):
            #print('timestep %d' %(tt+1))
            infected = disease_spread(Net, infected, NN, pp[ii], rr)
            num_inf[tt+1] = np.count_nonzero(infected)
        final_num[ii] = num_inf[-1]
        plt.plot(num_inf)

    plt.xlabel('timestep t')
    plt.ylabel('Number of infected individuals')

    plt.show()

    plt.clf()

    plt.scatter(rr/pp.astype(float), final_num)
    plt.xlabel('Probability ratio r/p')
    plt.ylabel('Number of infected people at day 1000')

    plt.show()





infectprob()
