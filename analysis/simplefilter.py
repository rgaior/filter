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
import waveform
import analyse

#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)

givensnr = 0.3
givensiglength = 100e-9

sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.setpowerenvelope('gauss')
sim.producesignal()

thesignal = sim.noise + sim.signal

simwf = waveform.Waveform(sim.time,thesignal, type='hf')
wf = det.producesimwaveform(simwf,'adc')

an =analyse.Analyse(det = det)
wattwf = an.producepowerwaveform(wf)
sigmawf = an.producesigmawaveform(wattwf)
filtwattwf = an.lowpass(wattwf,3e6,7)
sigmafiltwf = an.producesigmawaveform(filtwattwf)

fig1 = plt.figure(figsize = (8,8))
ax1 = plt.subplot(111)
#ax1.plot(wattwf.time, wattwf.amp,label=wattwf.type)
ax1.plot(sigmawf.time, sigmawf.amp,label=sigmawf.type)
ax1.plot(sigmafiltwf.time, sigmafiltwf.amp,label=sigmafiltwf.type)

plt.legend()
plt.show()
