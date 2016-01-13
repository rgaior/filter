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
wf = det.produceresponse(simwf)

fig1 = plt.figure(figsize = (8,8))
plt.subplot(211)
plt.plot(simwf.time*1e6, simwf.amp)
plt.xlabel('time [us]')
plt.ylabel('amplitude [V]')
plt.subplot(212)
plt.plot(wf.time*1e6, wf.amp)
plt.xlabel('time [us]')
plt.ylabel('power [dBm]')

plt.show()
