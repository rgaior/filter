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
plt.subplot(211)
plt.plot(sim.time*1e6, thesignal)
plt.xlabel('time [us]')
plt.ylabel('amplitude [V]')
plt.subplot(212)
plt.plot(x*1e6, wf)
plt.xlabel('time [us]')
plt.ylabel('power [dBm]')

mean = np.mean(wf)
std = np.std(wf)

# fig2 = plt.figure()
# ax1 = plt.subplot(111)
# n1, bins1, patches1 = ax1.hist(wf, 50, facecolor='red', alpha=0.75)
# ax1.text(0.95, 0.90, 'mean = ' + str(mean) + '\n' + 'std = '+ str(std),
#         verticalalignment='bottom', horizontalalignment='right',
#         transform=ax1.transAxes,
#         color='black', fontsize=15)

plt.show()
