import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

sim = simulation.Simulation(det=det, snr=10, siglength = 50e-9)

sim.producetime()
sim.producenoise()

fig1 = plt.figure(figsize = (8,8))
ax1 = plt.subplot2grid((2,2), (0,0), colspan=2)
ax2 = plt.subplot2grid((2,2), (1,0))
ax3 = plt.subplot2grid((2,2), (1,1))

ax1.plot(sim.time*1e6, sim.noise)
ax1.set_xlabel('time [us]',fontsize =15)
ax1.set_ylabel('amplitude [V]',fontsize =15)
n, bins, patches = ax2.hist(sim.noise, 50, facecolor='green', alpha=0.75)
#ax2.xaxis.set_major_locator(ticker.MultipleLocator( (np.max(sim.noise) -np.min(sim.noise))/2))
ax2.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
ax2.set_xlabel('amplitude [V]',fontsize =15)
ax2.set_ylabel('entries',fontsize =15)
mvnoise = np.mean(sim.noise)
stdvnoise = np.std(sim.noise)
pnoise = sim.noise*sim.noise/50
n1, bins1, patches1 = ax3.hist(pnoise, 50, facecolor='red', alpha=0.75)
ax3.set_xlabel('power [W]',fontsize =15)
#ax3.set_ylabel('entries',fontsize =15)
mpnoise = np.mean(pnoise)
ax1.text(0.95, 0.90, 'Tsys = '+ str("%.2f" % tsys) + ' K',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax1.transAxes,
        color='black', fontsize=15)
ax2.text(0.95, 0.90, 'mean = '+ str("%.2g" % mvnoise),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax2.transAxes,
        color='black', fontsize=12)
ax2.text(0.95, 0.85, 'std = '+ str("%.2g" % stdvnoise),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax2.transAxes,
        color='black', fontsize=12)
ax3.text(0.95, 0.90, 'mean = '+ str("%.2g" % mpnoise),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax3.transAxes,
        color='black', fontsize=12)


#stdvnoise = np.std(sim.noise)
# plt.xlabel('power at installation [dBm]', fontsize =15)
# plt.ylabel('entries',fontsize = 15)
# plt.legend(fontsize=15)


plt.show()
