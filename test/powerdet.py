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
plt.subplot(311)
plt.plot(sim.time*1e6, thesignal)
plt.xlabel('time [us]')
plt.ylabel('amplitude [V]')
plt.subplot(312)
plt.plot(x*1e6, wf)
plt.xlabel('time [us]')
plt.ylabel('power [dBm]')
pdvoltage = det.powerdetlinear(wf)
plt.subplot(313)
plt.plot(x*1e6,pdvoltage)
plt.xlabel('time [us]')
plt.ylabel('power det amplitude [V]')


plt.show()
