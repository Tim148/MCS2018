import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.spatial import distance
import random as rnd
import os

def initdomain(NN, LL, vv):
    particles = np.random.uniform(0,LL,(NN,2))
    dir_angle = 2 * math.pi * np.random.uniform(0,1,NN)
    velocity = np.zeros((NN,2))
    velocity[:,0] = vv * np.cos(dir_angle)
    velocity[:,1] = vv * np.sin(dir_angle)

    return particles, velocity, dir_angle

def nearneigh(nn, LL, particles):
    nmatrix = distance.squareform(distance.pdist(particles))
    nmatrix = np.argsort(nmatrix, axis=1)
    nmatrix = nmatrix[:,1:(nn+1)]
    return nmatrix

def runsim(particles, dir_angle, mass_center, gfac, vv, LL, NN, ee, nn):
    velocity = np.zeros((NN,2))
    nparticles = np.copy(particles)
    ndir_angle = np.copy(dir_angle)
    nneighbours = nearneigh(nn, LL, particles)
    for jj in range(NN):
        ss = 0
        sc = 0
        #grav_angle = math.acos(np.dot(particles[jj,:]/np.linalg.norm(particles[jj,:]), mass_center/np.linalg.norm(mass_center)))
        for ii in range(nn):
            ss = ss + math.sin(dir_angle[nneighbours[jj,ii]])
            sc = sc + math.cos(dir_angle[nneighbours[jj,ii]])
        ndir_angle[jj] = math.atan2(ss, sc) + rnd.uniform(-ee,ee)
        velocity[jj,:] = (mass_center - particles[jj,:])/np.linalg.norm(mass_center - particles[jj,:])

    velocity[:,0] = np.cos(ndir_angle) + gfac * velocity[:,0]
    velocity[:,1] = np.sin(ndir_angle) + gfac * velocity[:,1]
    for ii in range(NN):
        velocity[ii,:] = vv * velocity[ii,:]/np.linalg.norm(velocity[ii,:])
    nparticles[:,0] = (particles[:,0] + vv * velocity[:,0])%LL
    nparticles[:,1] = (particles[:,1] + vv * velocity[:,1])%LL


    return nparticles, velocity, ndir_angle

def test():
    nruns = 100
    JJ = 200

    LL = 10
    ee = np.arange(0.1,4.1,0.1)
    NN = 40 # Number of particles
    nn = np.arange(0,NN,1) # Number of nearest Neighbours

    print(ee.size)
    print(nn.size)

    vv = 0.5
    gfac = 0.1
    galign = np.zeros((JJ,nruns))
    avgalign = np.zeros(JJ-1)
    steadystate = np.zeros((ee.size, nn.size))
    #particles, velocity, dir_angle = initdomain(NN, LL, vv)
    #mass_center = np.array([np.average(particles[:,0]), np.average(particles[:,1])])


    for kk in range(ee.size):
        print('%d. e value' %(kk+1))
        for ll in range(nn.size):
            print('%d. n value' %(ll+1))

            for ii in range(nruns):
                #print('%d. Simulation' %ii)
                particles, velocity, dir_angle = initdomain(NN, LL, vv)
                mass_center = np.array([np.average(particles[:,0]), np.average(particles[:,1])])
                avgvel = np.sum(velocity, axis=0)/float(NN*vv)
                galign[0,ii] = np.linalg.norm(avgvel)
                avgalign[0] = np.average(galign[0,:])
                for tt in range(JJ-1):
                    particles, velocity, dir_angle = runsim(particles, dir_angle, mass_center, gfac, vv, LL, NN, ee[kk], nn[ll])
                    mass_center = np.array([np.average(particles[:,0]), np.average(particles[:,1])])
                    avgvel = np.sum(velocity, axis=0)/float(NN*vv)
                    galign[tt+1,ii] = np.linalg.norm(avgvel)
                    avgalign[tt] = np.average(galign[tt,:])
            #print(avgalign)
            steadystate[kk,ll] = avgalign[-1]


    plt.imshow(steadystate, origin='lower')
    plt.xlabel('angular error e')
    plt.ylabel('number of nearest neighbours n')
    plt.colorbar()
    plt.show()


def gfactest():
    nruns = 100
    JJ = 200

    ee = 0.5
    NN = 40 # Number of particles
    nn = 4 # Number of nearest Neighbours
    LL = 10
    vv = 0.5
    gfac = np.arange(0.01, 0.11, 0.01)
    galign = np.zeros((JJ,nruns))
    avgalign = np.zeros(JJ)
    for jj in range(gfac.size):
        print('force = %f' %gfac[jj])
        for ii in range(nruns):
            #print('%d. Simulation' %ii)
            particles, velocity, dir_angle = initdomain(NN, LL, vv)
            mass_center = np.array([np.average(particles[:,0]), np.average(particles[:,1])])
            avgvel = np.sum(velocity, axis=0)/float(NN*vv)
            galign[0,ii] = np.linalg.norm(avgvel)
            for tt in range(JJ-1):
                particles, velocity, dir_angle = runsim(particles, dir_angle, mass_center, gfac[jj], vv, LL, NN, ee, nn)
                avgvel = np.sum(velocity, axis=0)/float(NN*vv)
                galign[tt+1,ii] = np.linalg.norm(avgvel)

    #plt.quiver(particles[:,0], particles[:,1], velocity[:,0], velocity[:,1], headlength = 1, headwidth =1, width = 0.005, pivot = 'tip', minlength=0.1, scale=15)
    #plt.scatter(particles[:,0], particles[:,1], color='black', marker='.')
        for tt in range(JJ):
            avgalign[tt] = np.average(galign[tt,:])

        plt.plot(avgalign)

    plt.xlabel('timestep t')
    plt.ylabel('global alignment')
    plt.show()

test()
