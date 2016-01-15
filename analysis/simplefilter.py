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

if len(sys.argv) != 4:
    print 'usage: python simplefilter <snr> <signal length [s]> <filter cut>' 
    sys.exit()
    
givensnr = float(sys.argv[1])
givensiglength = float(sys.argv[2])
filterfcut  = float(sys.argv[3])

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
filtwattwf = an.lowpasshard(wattwf,filterfcut)
sigmafiltwf = an.producesigmawaveform(filtwattwf)

specori = np.absolute(np.fft.rfft(wattwf.amp)) 
specfilt = np.absolute(np.fft.rfft(filtwattwf.amp)) 

freq  = np.fft.rfftfreq(len(wattwf.amp),1/wattwf.sampling)

fig1 = plt.figure(figsize = (8,5))
ax1 = plt.subplot(111)
ax1.plot(sigmawf.time*1e6, sigmawf.amp,label='original')
ax1.plot(sigmafiltwf.time*1e6, sigmafiltwf.amp,lw=2,label='filtered < '+ str("%.2g" % filterfcut + ' Hz'))
ax1.set_xlabel('time [us]',fontsize=15)
ax1.set_ylabel('power [sigma]',fontsize=15)
# ax2 = plt.subplot(212)
# ax2.semilogy(freq, specori*specori,label='original')
# ax2.semilogy(freq, specfilt*specfilt,label='filtered')
ax1.text(0.95, 0.95, 'snr = ' + str(givensnr) + ', signal length = ' + str("%.2g" % givensiglength) + ' s',
         verticalalignment='top', horizontalalignment='right',
         transform=ax1.transAxes,
         color='red', fontsize=15)

plt.legend(loc=4)
plt.show()
