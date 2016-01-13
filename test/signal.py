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

#usage:
if len(sys.argv) != 3:
    print 'usage: python signal  <snr>  <signallength [s]>'
    sys.exit()
givensnr = float(sys.argv[1])
givensiglength = float(sys.argv[2])
sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.setpowerenvelope('gauss')
sim.producesignal()

fig1 = plt.figure(figsize = (8,8))
ax1 = plt.subplot2grid((3,1), (0,0))
ax2 = plt.subplot2grid((3,1), (1,0))
ax3 = plt.subplot2grid((3,1), (2,0))

ax1.plot(sim.time*1e6, sim.noise)
ax1.set_xlabel('time [us]',fontsize =15)
ax1.set_ylabel('amplitude [V]',fontsize =15)

ax2.plot(sim.time*1e6, sim.signal)
ax2.set_xlabel('time [us]',fontsize =15)
ax2.set_ylabel('amplitude [V]',fontsize =15)

ax3.plot(sim.time*1e6, sim.signal +sim.noise)
ax3.set_xlabel('time [us]',fontsize =15)
ax3.set_ylabel('amplitude [V]',fontsize =15)
# ax1.text(0.95, 0.90, 'Tsys = '+ str("%.2f" % tsys) + ' K',
#         verticalalignment='bottom', horizontalalignment='right',
#         transform=ax1.transAxes,
#         color='black', fontsize=15)
ax2.text(0.95, 0.05, 'signal length = ' + str("%.2g" % givensiglength),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax2.transAxes,
        color='red', fontsize=12)
ax2.text(0.95, 0.15, 'snr = '+ str("%.2f" % givensnr) ,
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax2.transAxes,
        color='red', fontsize=12)
ax1.text(0.95, 0.85, 'noise',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax1.transAxes,
        color='black', fontsize=15)
ax2.text(0.95, 0.85, 'signal',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax2.transAxes,
        color='black', fontsize=15)
ax3.text(0.95, 0.85, 'signal + noise',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax3.transAxes,
        color='black', fontsize=15)
# ax3.text(0.95, 0.90, 'mean = '+ str("%.2g" % mpnoise),
#         verticalalignment='bottom', horizontalalignment='right',
#         transform=ax3.transAxes,
#         color='black', fontsize=12)


#stdvnoise = np.std(sim.noise)
# plt.xlabel('power at installation [dBm]', fontsize =15)
# plt.ylabel('entries',fontsize = 15)
# plt.legend(fontsize=15)


plt.show()
