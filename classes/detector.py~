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
        

        self.pd_k = 0.74
        self.pd_slope = -0.023
#     def reset(self):
#         self.time = []
#         self.horndet = []
        
    def produceresponse(self,signal):
        tend = 500e-9
        sampling = 5e9 
        period = 1./sampling
        x = np.arange(0,tend,period)
        convfunc = period*np.exp(-x/self.tau)/( -(math.exp(-tend/self.tau) - 1)*self.tau)
        signal = 10*np.log10(self.gain*signal*signal/constant.impedance)
        resp = np.convolve(signal,convfunc,'valid')
        #resp = np.convolve(signal,convfunc) 
#        return 0.74 - 0.023*(resp+30)
        return resp+30


    def powerdetlinear(self, signal):
        return self.pd_k + self.pd_slope*signal
