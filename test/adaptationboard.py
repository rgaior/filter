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
sim.setpowerenvelope('gauss')
sim.producesignal()

thesignal = sim.noise + sim.signal

simwf = waveform.Waveform(sim.time,thesignal, type='hf')
pdwf = det.producesimwaveform(simwf,'powerdetector')

boardwf = det.adaptationboard(pdwf)

fig1 = plt.figure(figsize = (8,8))
ax1 = plt.subplot(311)
ax1.plot(simwf.time*1e6, simwf.amp)
ax1.set_ylabel('amplitude [V]',fontsize=15)

ax2 = plt.subplot(312,sharex = ax1)
ax2.plot(pdwf.time*1e6, pdwf.amp)
#ax2.set_xlabel('time [us]')
ax2.set_ylabel('power det. [V]',fontsize=15)
ax3 = plt.subplot(313,sharex=ax1)
ax3.plot(boardwf.time*1e6,boardwf.amp)
ax3.set_xlabel('time [us]',fontsize=15)
ax3.set_ylabel('board amplitude [V]',fontsize=15)


plt.show()
