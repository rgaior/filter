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
x = np.linspace(0, float(len(wf))/sim.sampling, len(wf))
fig1 = plt.figure(figsize = (8,8))

ax1 = plt.subplot(311)
ax1.plot(sim.time*1e6, thesignal)
#ax1.set_xlabel('time [us]')
ax1.set_ylabel('amplitude [V]',fontsize=15)

ax2 = plt.subplot(312,sharex = ax1)
ax2.plot(x*1e6, wf)
#ax2.set_xlabel('time [us]')
ax2.set_ylabel('power [dBm]',fontsize=15)
pdvoltage = det.powerdetlinear(wf)
adaptvoltage = det.adaptationboard(pdvoltage)
ax3 = plt.subplot(313,sharex=ax1)
ax3.plot(x*1e6,adaptvoltage)
ax3.set_xlabel('time [us]',fontsize=15)
ax3.set_ylabel('board amplitude [V]',fontsize=15)


plt.show()