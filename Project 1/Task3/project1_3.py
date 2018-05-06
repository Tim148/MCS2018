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

def deriv(AA, bb, nn):
    deriv = (((bb*AA)/nn) * math.exp(-(AA/nn)) * (1 - AA/(2*nn)))

    return deriv

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

def Lyapunov():
    nn = 1000
    ncalc = 1000.0
    bb = np.arange(1, 101, 1)
    A_init = nn
    TT = 10000
    AA = np.zeros((TT,bb.size))
    lyap = np.zeros(bb.size, dtype=float)


    d_da = np.zeros((TT,bb.size))

    for jj in range(bb.size):
        site = initsite(A_init, nn)
        AA[0,jj] = A_init
        d_da[0,jj] = deriv(AA[0,jj], bb[jj], ncalc)
        nT = TT
        print('%d. Simulation' %(jj+1))
        for tt in range(TT-1):
            (AA[tt+1,jj], site) = popsim(nn, bb[jj], site)
            d_da[tt+1,jj] = deriv(AA[tt+1,jj], bb[jj], ncalc)
            if d_da[tt+1,jj] != 0:
                lyap[jj] = lyap[jj] + math.log(math.fabs(d_da[tt+1,jj]))
            else:
                nT = nT - 1

                #lyap[jj] = lyap[jj] + math.log((((bb[jj]*AA[tt+1,jj])/ncalc) * math.exp(-(AA[tt+1,jj]/ncalc)) * (1 - AA[tt+1,jj]/(2*ncalc))))
        lyap[jj] = lyap[jj]/nT

    plt.plot(lyap)
    plt.xlabel('b')
    plt.ylabel('$\lambda$')
    plt.show()

Lyapunov()
