import utils
import math
import numpy as np
import constant
import waveform
import detector
from scipy import signal

class Analyse:
    def __init__(self, det = None):
        self.det = det
        

    def producepowerwaveform(self, wf):
        vfeamp = utils.adctov_board(wf.amp)
        powerdet = (vfeamp-self.det.board_k)/self.det.board_slope
        pdbm = (powerdet - self.det.pd_k)/self.det.pd_slope
        watt = utils.dbmtowatt(pdbm)
        newwf = waveform.Waveform(wf.time,watt,'an_watt')
        return newwf
        
    def producesigmawaveform(self, wf):
        size = len(wf.amp)
        mean = np.mean(wf.amp[size/2:size*0.7])
        std = np.std(wf.amp[size/2:size*0.7])
        sigma = (wf.amp - mean)/std
        newwf = waveform.Waveform(wf.time,sigma,'an_sigma')
        return newwf

    def producemeanwaveform(self, wf):
        size = len(wf.amp)
        mean = np.mean(wf.amp[size/2:])
        std = np.std(wf.amp[size/2:])
        mean = (wf.amp)/mean
        newwf = waveform.Waveform(wf.time,mean,'an_mean')
        return newwf


    def lowpass(self, wf, fcut, order):
        filtamp = utils.lowpass(wf.amp,wf.sampling,order,fcut)
        newwf = waveform.Waveform(wf.time,filtamp,'an_filt')
        return newwf

    def lowpasshard(self, wf, fcut):
        filtamp = utils.lowpasshard(wf.amp,wf.sampling,fcut)
        newwf = waveform.Waveform(wf.time,filtamp,'an_filt')
        return newwf

    def crosscorrel(self, wf, envelopewf):
        newenv = np.interp(wf.time, envelopewf.time, envelopewf.amp/np.max(envelopewf.amp))
        crosscorrel = signal.correlate(wf.amp, newenv, mode='full')
        #here we cut the correlated waveform. 
        # it is not really clean now, but we select the window of the input size with the largest integral
        size = len(wf.time)
        halfccsize = int(len(crosscorrel)/2)
        goodindexstart = 0
        goodindexstop = 0
        maxint = -1.
        for i in range(halfccsize):
            indexstart = i
            indexstop = i+size
            newc = crosscorrel[indexstart:indexstop]
            if np.sum(newc) > maxint:
                maxint = np.sum(newc)
                goodindexstart = indexstart
                goodindexstop = indexstop
        newc = crosscorrel[goodindexstart:goodindexstop]
        newwf = waveform.Waveform(wf.time,newc,'an_correl')
        return newwf
