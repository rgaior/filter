import numpy as np
import math




###############################################
####  reading functions                 #####
###############################################

# read a file with: time power [W]
def readsimfile(file):
    f = open(file,'r+')
    time = np.array([])
    power = np.array([])
    for l in f:
        lsplit = l.split()
        time = np.append(time,float(lsplit[0]))
        power = np.append(power,float(lsplit[1]))
    return [time,power]



###############################################
####  producing functions                 #####
###############################################


def wf_normal(mean,sigma,nrofsamples):
    return np.random.normal(mean,sigma,nrofsamples)


def func_normedgauss(x,mean,sigma):
    #a = (1./(sigma*( math.sqrt(2*math.pi) )) )*np.exp(-0.5* ((x - mean)/sigma)**2 )
    a = np.exp(-0.5* ((x - mean)/sigma)**2 )
    return a



