import utils
import math
import numpy as np
from scipy import signal
import constant

class Detector:
    def __init__(self, temp, gain, bw, tau):
        self.temp = temp
        self.gain = gain
        self.bw = bw
        self.tau = tau
        

        #cf thesis R.Gaior for the numbers
        self.pd_k = 0.74
        self.pd_slope = -0.023
        #cf depends on board,
        #take an example for now
        self.board_k = 5.5
        self.board_slope = -4.1
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

#power detector characteristic (P[dBm] vs V_pd[V])
    def powerdetlinear(self, signal):
        return self.pd_k + self.pd_slope*signal
#adaptation board characteristic (V_pd [V] vs V_board [V])
    def adaptationboard(self, signal):
        return self.board_k + self.board_slope*signal
#simulate the Front end filter of Auger electronics 
    def FEfilter(self, sig, sampling):
        Nyfreq = sampling/2
        fcut = 20e6 #[Hz]
        ratiofreq = float(fcut)/Nyfreq
        b, a = signal.butter(4, ratiofreq)
        y = signal.filtfilt(b, a, sig)
        return y

#simulate:
    # the sampling in time (every 25ns)
    def FEtimesampling(self, time, signal):
        #first time sampling:
        step = 25e-9
        tracelength = time[-1] - time[0]
        nrofpoints = int(tracelength/step)
        newtime = np.linspace(time[0],time[-1],nrofpoints)
        newy = np.interp(newtime,time,signal)
        return [newtime,newy]

#simulate
    # the gain of the input amplifier g = (-1/2)
    # the sampling in amplitude (0-1 to 0-1023)
    def FEampsampling(self, signal):
        #first time sampling:
        newy = -0.5*signal*1023
        newy = newy.astype(int)
        return newy
