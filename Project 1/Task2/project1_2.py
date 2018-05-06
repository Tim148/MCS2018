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
        AA_mf[tt+1] = meanfield(AA_mf[tt], bb, nn)

    return AA_mf

def Atp1oAt():
    nn = 1000.0
    bb = np.array([5.4, 5.5, 6.0, 6.5, 7.0, 7.5])
    AA_init = int(nn)
    TT = 1000

    Atp1 = np.zeros((TT,bb.size))
    At = np.arange(0,TT+1,1)

    fig, axes = plt.subplots(2,3)
    plt.subplots_adjust(wspace=0.6, hspace=0.6)

    for jj in range(bb.size):
        print('Simulations for b = %f' %(bb[jj]))
        for ii in range(TT):
            Atp1[ii,jj] = (bb[jj]/(2*nn))* At[ii]**2 * math.exp(-(At[ii]/nn))
        axes[int(jj>2), jj%3].plot(Atp1[:,jj])
        axes[int(jj>2), jj%3].plot(At, linestyle=':')
        axes[int(jj>2), jj%3].set_title('b = %f' %bb[jj])
        axes[int(jj>2), jj%3].set(xlabel='$a_t$', ylabel='$a_{t+1}$')

    plt.show()

def steady_states():
    nn = 1000.0
    bb = 7.0
    AA_init = int(500)
    Steps = 6000
    TT = 100
    factor = 0.01

    xx = np.zeros(TT)
    yy = np.zeros(TT)
    xx[0]= AA_init

    site = initsite(AA_init, int(nn))

    Atp1 = np.zeros(Steps)
    At = np.arange(0,Steps,1)

    for ii in range(Steps):
        Atp1[ii] = (bb/(2*nn))* At[ii]**2 * math.exp(-(At[ii]/nn))

    fig, axes = plt.subplots(1,2)
    plt.subplots_adjust(wspace=0.6, hspace=0.6)

    xx1 = 1900.0
    yy1 = 1900.0

    xx2 = 420.0
    yy2 = 420.0


    axes[0].plot(Atp1)
    axes[0].plot(At, linestyle=':')
    axes[0].scatter(xx1,yy1, marker='x', color='black')
    axes[0].set_title('First new steady state in more detail')
    axes[0].set(xlabel='$a_t$', ylabel='$a_{t+1}$')
    axes[1].plot(Atp1[0:1000])
    axes[1].plot(At[0:1000], linestyle=':')
    axes[1].set_title('Second new steady state in more detail')
    axes[1].set(xlabel='$a_t$', ylabel='$a_{t+1}$')
    axes[1].scatter(xx2,yy2, marker='x', color='black')
    plt.show()

def intersect():
    nn = 1000.0
    bb = np.arange(5.5,20,0.1)
    AA_init = int(500)
    Steps = 10000

    bb1 = np.zeros(bb.size)
    bb2 = np.zeros(bb.size)

    site = initsite(AA_init, int(nn))

    #min = np.zeros(bb.size)
    Atp1 = np.zeros((Steps, bb.size))
    At = np.arange(0,Steps,1)

    for jj in range(bb.size):
        for ii in range(Steps):
            Atp1[ii,jj] = (bb[jj]/(2*nn))* At[ii]**2 * math.exp(-(At[ii]/nn))
        Atp1[:,jj] = Atp1[:,jj] - At
        Atp1[:,jj] = np.absolute(Atp1[:,jj])
        min = np.amin(Atp1[5:1000,jj])
        ns1 = np.nonzero((Atp1[:,jj]==min))
        ns1 = ns1[0]
        bb1[jj] = ns1
        min = np.amin(Atp1[1000:-1,jj])
        ns2 = np.nonzero((Atp1[:,jj]==min))
        ns2 = ns2[0]
        bb2[jj] = ns2

    plt.scatter(bb, bb1, marker='.')
    plt.scatter(bb, bb2, marker ='.')
    plt.xlabel('b')
    plt.ylabel('$a_t$ of steady states')
    #plt.plot(bb1)
    plt.show()


    #plt.plot(Atp1)
    #plt.plot(np.zeros(Steps), linestyle=':')
    #plt.show()

intersect()
