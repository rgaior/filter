import utils
import math
import numpy as np
from scipy import signal
import constant
import waveform
#hard coded value:
#front end filter cut frquency
fcut = 20e6
fesampling = 40e6
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
        
    #return [time, amp] for the different stages of the detector
    def producesimwaveform(self, simwf, stage):
        stagelc = stage.lower()
        if stagelc not in ['logresponse','powerdetector','board','fefilter','timesampled','adc']:
            print 'choose among these stages: \n ', 'logresponse or powerdetector or board or fefilter or timesampled or adc'
            return 
        elif stagelc == 'logresponse':
            return self.produceresponse(simwf)
        elif stagelc == 'powerdetector':
            logresponse = self.produceresponse(simwf)
            return self.powerdetlinear(logresponse)
        elif stagelc == 'board':
            logresponse = self.produceresponse(simwf)
            afterpd = self.powerdetlinear(logresponse)
            return self.adaptationboard(afterpd)
        elif stagelc == 'fefilter':
            logresponse = self.produceresponse(simwf)
            afterpd = self.powerdetlinear(logresponse)
            afterboard = self.adaptationboard(afterpd)
            return self.FEfilter(afterboard)
        elif stagelc == 'timesampled':
            logresponse = self.produceresponse(simwf)
            afterpd = self.powerdetlinear(logresponse)
            afterboard = self.adaptationboard(afterpd)
            afterFEfilter = self.FEfilter(afterboard)
            return self.FEtimesampling(afterFEfilter)
        elif stagelc == 'adc':
            logresponse = self.produceresponse(simwf)
            afterpd = self.powerdetlinear(logresponse)
            afterboard = self.adaptationboard(afterpd)
            afterFEfilter = self.FEfilter(afterboard)
            timesampled = self.FEtimesampling(afterFEfilter)
            return self.FEampsampling(timesampled)

    def produceresponse(self,wf):
        tend = 500e-9
        period = 1./wf.sampling
        x = np.arange(0,tend,period)
        convfunc = period*np.exp(-x/self.tau)/( -(math.exp(-tend/self.tau) - 1)*self.tau)
        # response in dBm
        signal = 10*np.log10(self.gain*(wf.amp*wf.amp)/constant.impedance) +30
        resp = np.convolve(signal,convfunc,'valid')
        newtime = np.linspace(wf.time[0], float(len(resp))/wf.sampling, len(resp))
        newamp = resp
        newwf = waveform.Waveform(newtime,newamp,'logresponse')
        return newwf

#power detector characteristic (P[dBm] vs V_pd[V])
    def powerdetlinear(self, wf):
        newwf = waveform.Waveform(wf.time,self.pd_k + self.pd_slope*wf.amp,'powerdetector')
        return newwf
#adaptation board characteristic (V_pd [V] vs V_board [V])
    def adaptationboard(self, wf):
        newwf = waveform.Waveform(wf.time,self.board_k + self.board_slope*wf.amp,'board')
        return newwf
#simulate the Front end filter of Auger electronics 
    def FEfilter(self, wf):
        Nyfreq = wf.sampling/2
        ratiofreq = float(fcut)/Nyfreq
        b, a = signal.butter(4, ratiofreq)
        y = signal.filtfilt(b, a, wf.amp)
        newwf = waveform.Waveform(wf.time,y,'fefilter')
        return newwf

#simulate:
    # the sampling in time (every 25ns)
    def FEtimesampling(self, wf):
        #first time sampling:
        step = float(1./fesampling)
        tracelength = wf.length
        nrofpoints = int(tracelength/step)
        newtime = np.linspace(wf.tstart,wf.tend,nrofpoints)
        newy = np.interp(newtime,wf.time,wf.amp)
        newwf = waveform.Waveform(newtime,newy,'timesampled')
        return newwf

#simulate
    # the gain of the input amplifier g = (-1/2)
    # the sampling in amplitude (0-1 to 0-1023)
    def FEampsampling(self, wf):
        #first time sampling:
        newy = -0.5*wf.amp*1023
        newy = newy.astype(int)
        newwf = waveform.Waveform(wf.time,newy,'adc')
        return newwf
