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
import analyse

#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)

if len(sys.argv) != 3:
    print 'usage: python simplefilter <snr> <signal length [s]> ' 
    sys.exit()
    
givensnr = float(sys.argv[1])
givensiglength = float(sys.argv[2])
#fcuts = [0.5e6, 1e6, 2e6, 4e6, 10e6] 
fcuts = [1e6, 2e6, 10e6] 

sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.setpowerenvelope('gauss')
sim.producesignal()

thesignal = sim.noise + sim.signal

simwf = waveform.Waveform(sim.time,thesignal, type='hf')
wf = det.producesimwaveform(simwf,'adc')

an =analyse.Analyse(det = det)
wattwf = an.producepowerwaveform(wf)
sigmawf = an.producesigmawaveform(wattwf)
fig1 = plt.figure(figsize = (8,5))
ax1 = plt.subplot(111)
ax1.plot(sigmawf.time*1e6, sigmawf.amp,'k',label='original')
for fcut in  fcuts:
    filtwattwf = an.lowpasshard(wattwf,fcut)
    sigmafiltwf = an.producesigmawaveform(filtwattwf)

    ax1.plot(sigmafiltwf.time*1e6, sigmafiltwf.amp,lw=2,label='filtered < '+ str("%.2g" % fcut + ' Hz'))
    ax1.set_xlabel('time [us]',fontsize=15)
    ax1.set_ylabel('power [sigma]',fontsize=15)
# ax2 = plt.subplot(212)
# ax2.semilogy(freq, specori*specori,label='original')
# ax2.semilogy(freq, specfilt*specfilt,label='filtered')
ax1.text(0.95, 0.95, 'snr = ' + str(givensnr) + ', signal length = ' + str("%.2g" % givensiglength) + ' s',
         verticalalignment='top', horizontalalignment='right',
         transform=ax1.transAxes,
         color='red', fontsize=15)
ax1.set_xlim(0,10)
plt.legend(loc=4)
plt.show()
