import matplotlib.pyplot as plt
import numpy as np
import os
import sys
cwd = os.getcwd()
classpath = cwd + '/../classes/'
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
sys.path.append(classpath)
import utils
import simulation
import detector
from scipy.optimize import curve_fit
from scipy import signal

#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)

snr = 10
givensiglength = 30e-9
fig1 = plt.figure(figsize = (8,8))
snrafter = np.array([])
sim = simulation.Simulation(det=det, snr=snr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.producesignal()

thesignal = sim.noise + sim.signal
envelope = sim.envelope      
wf = det.produceresponse(thesignal)

crosscorrel = signal.correlate(wf, envelope, mode='same')
size = len(crosscorrel)
print size
xcross = np.arange(0,size,1)
fig1 = plt.figure()
plt.plot(xcross,crosscorrel)
fig2 = plt.figure()
xdet = np.arange(0,len(wf),1)
plt.plot(xdet,wf)
#plt.legend()
#mean = np.mean(wf)
#std = np.std(wf)

plt.show()
