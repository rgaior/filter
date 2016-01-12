import utils
import math
import numpy as np
import constant

class Simulation:
    def __init__(self, noisedist = '', 
                 snr = 0,
                 siglength = 0,
                 sigdist = '',
                 det = None,
                 ):

        self.det = det
        self.snr = snr
        self.noisedist = noisedist
        self.siglenth = siglength
        self.sigdist = sigdist
        
        self.time = np.array([])
        self.noise = np.array([])
        self.signal = np.array([])
        self.envelope = np.array([])
        self.wf = np.array([])
        
        #hardcoded
        self.tracelength = 10e-6 #s
        self.sampling = 5e9 #Hz
        self.sigtime = self.tracelength/4
        
#     def reset(self):
#         self.time = []
#         self.horndet = []
        
    def producetime(self):
        self.time = np.arange(0,self.tracelength,1./self.sampling)

    def producenoise(self):
        Pnoise = constant.kb*self.det.temp*self.det.bw 
        Vnoise = np.sqrt(constant.impedance*Pnoise)
        self.noise = utils.wf_normal(0,Vnoise,len(self.time))

    def producesignal(self):
        Pnoise = constant.kb*self.det.temp*self.det.bw 
        Vnoise = np.sqrt(constant.impedance*Pnoise)
        signal = utils.wf_normal(0,Vnoise,len(self.time))
        envelope = utils.func_normedgauss(self.time,self.sigtime,self.siglenth)
        self.envelope = envelope
        self.signal = envelope*math.sqrt(self.snr)*signal
