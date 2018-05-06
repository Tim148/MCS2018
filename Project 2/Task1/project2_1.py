import numpy as np
import matplotlib.pyplot as plt
import os
import random as rnd

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

def runfriends(nn, rr, TT):

    groups= np.zeros((nn,TT))

    groups[:,0] = initgroups(nn)

    for tt in range(TT-1):
        groups[:,tt+1] = simfriends(groups[:,tt], nn, rr)

    return groups[:,-1]

def finaldist():
    nruns = 50
    nn = 100
    rr = 0.01
    TT = 10000

    fdistr = np.zeros((nn,nruns))

    for ii in range(nruns):
        print('%d. Simulation' %(ii+1))
        fdistr[:,ii] = runfriends(nn, rr, TT)

    uniques, counts = np.unique(fdistr, return_counts='True')
    uniques = uniques[1:-1]
    counts = counts.astype(float)
    counts = counts[1:-1]
    counts = counts/(np.sum(counts))
    lu = np.log(uniques)
    lc = np.log(counts)

    print(uniques)
    print(counts)
    #plt.scatter(uniques[1:-1], counts[1:-1], marker='.')

    fig, axes = plt.subplots(1,2)
    plt.subplots_adjust(wspace=0.6, hspace=0.6)
    axes[0].scatter(uniques[1:-1], counts[1:-1], marker='.')
    axes[0].set_title('original representation')
    axes[0].set(xlabel='Groupsize', ylabel='frequency')
    axes[1].scatter(lu[1:-1], lc[1:-1], marker='.')
    axes[1].set_title('log-log representation')
    axes[1].set(xlabel='ln(Groupsize)', ylabel='ln(frequency)')

    plt.show()

def changeR():
    nruns = 100
    nn = 100
    #rr = np.arange(0.001,0.011,0.001)
    rr = np.array([0.001,0.01,0.1,0.5])
    print(len(rr))
    TT = 10000

    fdistr = np.zeros((nn,nruns,rr.size))

    fig, axes = plt.subplots(2,2)
    plt.subplots_adjust(wspace=0.6, hspace=0.6)

    #plotdict = {0:0,1:0,2:0,3:0,4:0,5:1,6:1,7:1,8:1,9:1}

    plotdict = {0:0,1:0,2:1,3:1}

    for jj in range(rr.size):
        print('%d. Simulation' %(jj+1))
        for ii in range(nruns):
            #print('%d.' %(ii+1))
            fdistr[:,ii,jj] = runfriends(nn, rr[jj], TT)

        uniques, counts = np.unique(fdistr[:,:,jj], return_counts='True')
        uniques = uniques[1:-1]
        counts = counts.astype(float)
        counts = counts[1:-1]
        counts = counts/(np.sum(counts))
        uniques = np.log(uniques)
        counts = np.log(counts)
        axes[plotdict[jj],jj%2].scatter(uniques[1:-1], counts[1:-1], marker='.')
        axes[plotdict[jj],jj%2].set_title('r = %f' %rr[jj])
        axes[plotdict[jj],jj%2].set(xlabel='ln(Groupsize)', ylabel='ln(frequency)')

    plt.show()

changeR()
