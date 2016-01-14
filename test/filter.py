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
noise = sim.noise

freq = np.fft.rfftfreq(len(sim.time), 1./sim.sampling)
filtered = utils.lowpass(noise,sim.sampling,6,1e8)
spec = np.absolute(np.fft.rfft(noise))
specfilt = np.absolute(np.fft.rfft(filtered))

fig1 = plt.figure(figsize = (8,8))
ax1 = plt.subplot(211)
ax1.plot(sim.time, noise)
ax1.plot(sim.time, filtered)

ax2 = plt.subplot(212)
ax2.loglog(freq, spec*spec)
ax2.loglog(freq, specfilt*specfilt)

#plt.legend()
plt.show()
