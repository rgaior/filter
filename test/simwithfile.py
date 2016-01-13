import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import sys
cwd = os.getcwd()
classpath = cwd + '/../classes/'
utilspath = cwd + '/../utils/'
datapath = cwd + '/../data/'
sys.path.append(utilspath)
sys.path.append(classpath)
import utils
import simulation
import detector

# power envelope file
file = 'testenvelope.txt'
envfile = datapath + file


#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)


sim = simulation.Simulation(det=det)


sim.producetime()
sim.producenoise()
sim.setpowerenvelopewithfile(envfile)
sim.producesignal()

fig1 = plt.figure(figsize = (8,8))
ax1 = plt.subplot2grid((3,1), (0,0))
ax2 = plt.subplot2grid((3,1), (1,0))
ax3 = plt.subplot2grid((3,1), (2,0))

ax1.plot(sim.time*1e6, sim.powerenvelope)
ax1.set_xlabel('time [us]',fontsize =15)
ax1.set_ylabel('power [W]',fontsize =15)
ax1.set_xlim(1,5)
#ax1.set_ylim(-100000*np.min(sim.powerenvelope),1.1*np.max(sim.powerenvelope))
ax1.set_ylim(-0.5*np.max(sim.powerenvelope),1.1*np.max(sim.powerenvelope))

ax2.plot(sim.time*1e6, sim.signal)
ax2.set_xlabel('time [us]',fontsize =15)
ax2.set_ylabel('amplitude [V]',fontsize =15)
ax2.set_xlim(1,5)

ax3.plot(sim.time*1e6, sim.signal +sim.noise)
ax3.set_xlabel('time [us]',fontsize =15)
ax3.set_ylabel('amplitude [V]',fontsize =15)
ax3.set_xlim(1,5)

ax1.text(0.95, 0.05, 'signal file = ' + file,
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax1.transAxes,
        color='red', fontsize=12)
ax1.text(0.95, 0.85, 'power envelope',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax1.transAxes,
        color='black', fontsize=15)
ax2.text(0.95, 0.85, 'signal in amplitude',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax2.transAxes,
        color='black', fontsize=15)
ax3.text(0.95, 0.85, 'signal + noise',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax3.transAxes,
        color='black', fontsize=15)


plt.show()
