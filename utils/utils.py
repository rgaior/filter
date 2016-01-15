import numpy as np
from scipy import signal
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

def wf_dirac(nrofsamples):
    return  np.append(np.array([1]),np.zeros(nrofsamples-1))


def func_normedgauss(x,mean,sigma):
    #a = (1./(sigma*( math.sqrt(2*math.pi) )) )*np.exp(-0.5* ((x - mean)/sigma)**2 )
    a = np.exp(-0.5* ((x - mean)/sigma)**2 )
    return a



###############################################
#### conversion function (voltage to adc, #####
#### voltage FE to voltage board etc... ) #####
###############################################
#for np array
#adc counts to volt at the FE input (between 0-1V)
def adctov_fe(adc):
    return adc.astype(float)/1024
def v_fetoadc(vfe):
    return vfe.astype(float)*1024

#voltage at front end to voltage at GIGAS/EASIER board
def v_fetov_board(vfe):
    return vfe*(-2)
def v_boardtov_fe(vboard):
    return vboard*(-1/2)

#adc to v board (between -2 and 0 V)
def adctov_board(adc):
    return v_fetov_board(adctov_fe(adc))
def v_boardtoadc(vboard):
    return v_fetoadc(v_boardtov_fe(vboard))


def dbmtowatt(dbm):
    return 10*np.power(10., (dbm - 30) /10)

def dbtowatt(db):
    return 10*np.power(10., db)

def watttodb(db):
    return 10*np.log10(db)

def watttodbm(dbm):
    return 10*np.log10(dbm)



###############################################
####              filtering               #####
###############################################

def lowpass(amp, sampling, order, fcut):
    Nyfreq = sampling/2
    ratiofcut = float(fcut)/Nyfreq
    b, a = signal.butter(order, ratiofcut, 'low')
    filtered = signal.filtfilt(b, a, amp)
    return filtered

def lowpasshard(amp, sampling, fcut):
    fft = np.fft.rfft(amp)
    freq = np.fft.rfftfreq(len(fft),float(1./sampling))
    Nyfreq = sampling/2
    min = np.min(np.absolute(fft))
    ratiofcut = float(fcut)/Nyfreq
    size = len(fft)
    newpass = fft[:int(ratiofcut*size)]
    sizeofzeros = size - len(newpass)
    newcut = np.zeros(sizeofzeros)
    newfft = np.append(newpass,newcut)
    out = np.fft.irfft(newfft)
    return out.real

def highpass(amp, sampling, order, fcut):
    Nyfreq = sampling/2
    ratiofcut = float(fcut)/Nyfreq
    b, a = signal.butter(order, ratiofcut, 'high')
    filtered = signal.filtfilt(b, a, amp)
    return filtered
