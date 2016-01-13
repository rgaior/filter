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
wf = det.producesimwaveform(simwf,'logresponse')
pdwf = det.powerdetlinear(wf)

fig1 = plt.figure(figsize = (8,8))
plt.subplot(311)
plt.plot(simwf.time*1e6, simwf.amp)
plt.xlabel('time [us]')
plt.ylabel('amplitude [V]')

plt.subplot(312)
plt.plot(wf.time, wf.amp)
plt.xlabel('time [us]')
plt.ylabel('power [dBm]')

plt.subplot(313)
plt.plot(pdwf.time*1e6,pdwf.amp)
plt.xlabel('time [us]')
plt.ylabel('power det amplitude [V]')


plt.show()
