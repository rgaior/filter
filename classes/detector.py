import utils
import math
import numpy as np
import constant

class Detector:
    def __init__(self, temp, gain, bw, tau):
        self.temp = temp
        self.gain = gain
        self.bw = bw
        self.tau = tau
        
#     def reset(self):
#         self.time = []
#         self.horndet = []
        
    def produceresponse(self,signal):
        tend = 500e-9
        sampling = 0.2e-9
        x = np.arange(0,tend,sampling)
        convfunc = np.exp(-x/self.tau)/( -(math.exp(-tend/self.tau) - 1)*self.tau)
        signal = 10*np.log10(signal*signal/constant.impedance)
        resp = np.convolve(signal,convfunc)*sampling
        return resp
