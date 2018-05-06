import numpy as np
import matplotlib.pyplot as plt
import os
import random as rnd
import math


def initsite(AA,nn):
    site = np.random.multinomial(AA, np.ones(nn)/nn, size=1)[0]
    return site

def popsim(nn, bb, site):
    new_pop = 0
    for ii in range(nn):
        if site[ii] == 2:
            new_pop = new_pop + bb
    new_site = np.random.multinomial(new_pop, np.ones(nn)/nn, size=1)[0]
    if np.sum(new_site) != new_pop:
        print('Error something went wrong')
        exit()
    return (new_pop, new_site)

def meanfield(AA, bb, nn):
    AA_new = ((bb * AA**2)/(2*nn)) * math.exp(-(AA/nn))
    return AA_new

def runsim(nn, bb, AA_init, TT):
    AA = np.zeros(TT)
    AA_mf = np.zeros(TT)
    AA[0] = AA_init
    AA_mf[0] = AA_init

    site = initsite(AA[0], nn)

    for tt in range(TT-1):
        (AA[tt+1], site) = popsim(nn, bb, site)
        AA_mf[tt+1] = meanfield(AA_mf[tt], bb, nn)

    return AA, AA_mf

def different_B():
    nn = 1000
    bb = np.array([5, 10, 20, 30, 40])
    AA_init = nn
    TT = 100
    AA = np.zeros((TT,bb.size))
    AA_mf = np.zeros((TT,bb.size))

    fig, axes = plt.subplots(2,3)
    plt.subplots_adjust(wspace=0.6, hspace=0.6)
    for ii in range(bb.size):
        AA[:,ii], AA_mf[:,ii] = runsim(nn, bb[ii], AA_init, TT)
        axes[int(ii>2), ii%3].plot(AA[:,ii])
        axes[int(ii>2), ii%3].set_title('b = %d' %bb[ii])
        axes[int(ii>2), ii%3].set(xlabel='timestep t', ylabel='Population $A_t$')

    axes[1,2].set_visible(False)
    plt.show()

def different_A():
    nn = 1000
    bb = 20
    AA_init = np.array([200, 100, 50, 10])
    TT = 100
    AA = np.zeros((TT,AA_init.size))
    AA_mf = np.zeros((TT,AA_init.size))

    fig, axes = plt.subplots(2,2)
    plt.subplots_adjust(wspace=0.6, hspace=0.6)
    for ii in range(AA_init.size):
        AA[:,ii], AA_mf[:,ii] = runsim(nn, bb, AA_init[ii], TT)
        axes[int(ii>1), ii%2].plot(AA[:,ii])
        axes[int(ii>1), ii%2].set_title('$A_0$ = %d' %AA_init[ii])
        axes[int(ii>1), ii%2].set(xlabel='timestep t', ylabel='Population $A_t$')

    #axes[1,2].set_visible(False)
    plt.show()

def phasetrans():
    nruns = 1000
    nn = 1000
    bb = np.arange(1, 51, 1)
    AA_init = nn
    TT = 100
    AA = np.zeros((TT,nruns,bb.size))
    AA_mf = np.zeros((TT,nruns,bb.size))
    A_values = np.zeros((100000, bb.size))
    A_counts = np.zeros((100000, bb.size))

    for ii in range(bb.size):
        print('Simulations for b = %d' %(ii+1))
        for jj in range(nruns):
            AA[:,jj,ii], AA_mf[:,jj,ii] = runsim(nn, bb[ii], AA_init, TT)
        uniques, counts = np.unique(AA[:,:,ii], return_counts=True)
        uniques = uniques.astype(int)
        A_counts[uniques,ii] = counts

    #plt.plot(A_counts[:,19])
    np.savetxt('Acounts.csv', A_counts)
    plt.imshow(A_counts, aspect='0.0005')
    plt.show()

def loadfile():
    A_counts = np.loadtxt('Acounts.csv')
    A_counts = (A_counts > 0)

    plt.imshow(A_counts[0:15000,:], aspect='0.003', cmap='binary', origin='lower')
    plt.xlabel('Reproduction parameter b')
    plt.ylabel('Population $A_t$')
    plt.show()


different_B()
