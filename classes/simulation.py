import utils
import math
import numpy as np
import constant
#import waveform

class Simulation:
    def __init__(self, snr = 0,
                 siglength = 0,
                 det = None):
        
        self.snr = snr
        self.det = det
        self.siglength = siglength
        
        self.powerenvelope = np.array([])
 
        self.time = np.array([])
        self.noise = np.array([])
        self.signal = np.array([])
        self.envelope = np.array([])
        self.wf = np.array([])
        
        #hardcoded
        self.tracelength = 20e-6 #s
        self.sampling = 5e9 #Hz
        self.sigtime = self.tracelength/4


    def producetime(self):
        self.time = np.arange(0,self.tracelength,1./self.sampling)
        
    #produce the noise samples (according gauss dist)
    def producenoise(self):
        Pnoise = constant.kb*self.det.temp*self.det.bw 
        Vnoise = np.sqrt(constant.impedance*Pnoise)
        self.noise = utils.wf_normal(0,Vnoise,len(self.time))
        
    # in case we want a simple fake signal
    # a gaussian is implemented as example
    def setpowerenvelope(self, type):
        if type == 'gauss':
            Pnoise = constant.kb*self.det.temp*self.det.bw 
            Psig = self.snr*Pnoise
            powerenvelope =  Psig*utils.func_normedgauss(self.time,self.sigtime,self.siglength)
        self.powerenvelope = powerenvelope

    # method to import a power profile from a file
    def setpowerenvelopewithfile(self, file):
        # get the envelope (time vs power [W]) from a file
        timepower = utils.readsimfile(file)
        # first shift the signal i.e. add or remove some time shift w.r.t. maximum
        # to set the max at the set value
        timeofmax = timepower[0][np.argmax(timepower[1])]
        timepower[0] = timepower[0] - timeofmax + self.sigtime
        # then resample
        # when the original array is smaller than the interpolated, the default interpolation done with numpy 
        # sets the outside points to the last value.
        # we want to be sure that the power outside the limit of the given signal is low (but not zero because of the future log10)
        maxfactor = 1e-10
        max = np.max(timepower[1])
        newamp = np.interp(self.time,timepower[0],timepower[1],left = maxfactor*max,right = maxfactor*max)
        powerenvelope = newamp
        self.powerenvelope = powerenvelope

    #produce the signal in time vs amplitude [V]
    def producesignal(self):
        signal = utils.wf_normal(0,1,len(self.time))
        self.signal = np.sqrt(self.powerenvelope*constant.impedance)*signal
