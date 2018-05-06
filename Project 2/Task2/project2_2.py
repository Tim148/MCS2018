import numpy as np
import matplotlib.pyplot as plt
import os
import random as rnd
import math

def initgroups(nn):
    groups = np.ones(nn)
    return groups

def simfriends(groups, nn, rr):
    gno = rnd.randint(0,nn-1)
    while groups[gno] == 0:
        gno = rnd.randint(0,nn-1)
    if groups[gno] == 1:
        pthresh = rnd.uniform(0,1)
        ind = np.random.choice(np.arange(0,nn), p = (groups/nn))
        groups[ind] = groups[ind] + 1
        groups[gno] = groups[gno] - 1
    elif groups[gno] > 1 and rnd.uniform(0,1) < groups[gno]*rr:
        inds = np.nonzero(groups == 0)
        inds = inds[0]
        for ii in range(int(groups[gno]-1)):
            groups[inds[ii]] = 1
            groups[gno] = groups[gno] - 1


    return groups

def MasterEQ(pi_1, pkmo, NN, rr, kk):
    #pi_k = ((pi_1/(NN*rr + pi_1))/kk)**(kk-1) * math.factorial(kk-1) * pi_1
    pi_k = (pi_1 * (kk-1) * pkmo)/(kk * (NN * rr + pi_1))

    return pi_k

def runfriends(nn, rr, TT):

    groups= np.zeros((nn,TT))

    groups[:,0] = initgroups(nn)

    for tt in range(TT-1):
        groups[:,tt+1] = simfriends(groups[:,tt], nn, rr)

    return groups[:,-1]

def finaldist():
    nruns = 200
    nn = 100
    rr = 0.01
    TT = 10000

    me_distr = np.zeros(nn+1)

    fdistr = np.zeros((nn,nruns))

    for ii in range(nruns):
        print('%d. Simulation' %(ii+1))
        fdistr[:,ii] = runfriends(nn, rr, TT)

    uniques, counts = np.unique(fdistr, return_counts='True')
    uniques = uniques[1:-1]
    counts = counts.astype(float)
    counts = counts[1:-1]
    counts = counts/(np.sum(counts))
    #lu = np.log(uniques)
    #lc = np.log(counts)


    plt.scatter(uniques[1:-1], counts[1:-1], marker='.')


    me_distr[0] = 0
    me_distr[1] = counts[0]

    print('calculating Master Equation')
    for ii in range(nn-1):
        me_distr[ii+2] = MasterEQ(me_distr[1], me_distr[ii+1], nn, rr, ii+2)

    plt.plot(me_distr[0:int(uniques[-1])], color='red')
    plt.xlim(xmin=1)
    plt.xlabel('Groupsize')
    plt.ylabel('frequency')

    plt.show()

finaldist()
