import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
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

#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)

givensnr = 10
givensiglength = 100e-9
sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.producesignal()

thesignal = sim.noise + sim.signal

wf = det.produceresponse(thesignal)
wf = det.powerdetlinear(wf)
wf = det.adaptationboard(wf)

x = np.linspace(0, float(len(wf))/sim.sampling, len(wf))
filt = det.FEfilter(wf,sim.sampling)
fig1 = plt.figure(figsize = (8,8))
ax1 = plt.subplot(211)
ax1.plot(x*1e6, wf,label='signal after adapt. board')
ax1.plot(x*1e6,filt,'r',lw=2,label='signal after FE filter')
ax1.set_xlim(1,3)
ax1.set_xlabel('time [us]')
ax1.set_ylabel('amplitude [V]',fontsize=15)
plt.legend()
ax2 = plt.subplot(212)
spec = np.abs(np.fft.rfft(wf))
specfilt = np.abs(np.fft.rfft(filt))
freq = np.fft.rfftfreq(len(x),x[1] - x[0])
#print spec

speccarre = spec*spec
specfiltcarre = specfilt*specfilt
ax2.loglog(freq*1e-6,speccarre)
ax2.loglog(freq*1e-6,specfiltcarre,'r')
ax2.set_xlabel('frequency [MHz]',fontsize=15)
ax2.set_ylabel('spectrum [a.u.]',fontsize=15)
ax2.plot(np.array([20,20]),[np.min(speccarre), np.max(specfiltcarre)],'k',lw=2)
ax2.set_ylim(1e-2,1e7)
plt.show()
