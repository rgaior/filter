import utils
import math
import numpy as np
from scipy import signal
import constant

class Waveform:
    def __init__(self, time = [], amp =[],type = ''):
        self.time = time
        self.amp = amp
        self.sampling = self.time[1] - self.time[0]
        self.tstart = self.time[0]
        self.tend = self.time[-1]
        self.length = self.tend - self.tstart
        self.type = type
        
