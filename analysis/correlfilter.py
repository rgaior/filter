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

givensnr = float(sys.argv[1])
givensiglength = float(sys.argv[2])

sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.setpowerenvelope('gauss')

sim.producesignal()

thesignal = sim.noise + sim.signal

simwf = waveform.Waveform(sim.time,thesignal, type='hf')
simenvwf = waveform.Waveform(sim.time,sim.powerenvelope, type='envelope')

wf = det.producesimwaveform(simwf,'adc')

an =analyse.Analyse(det = det)
wattwf = an.producepowerwaveform(wf)
sigmawf = an.producesigmawaveform(wattwf)
f1 = 1e6
f2 = 4e6
filtwattwf1 = an.lowpasshard(wattwf,f1)
filtwattwf2 = an.lowpasshard(wattwf,f2)
correlwattwf = an.crosscorrel(wattwf,simenvwf)

sigfiltwf1 = an.producesigmawaveform(filtwattwf1)
sigfiltwf2 = an.producesigmawaveform(filtwattwf2)
sigcorrelwf = an.producesigmawaveform(correlwattwf)

fig1 = plt.figure(figsize = (8,5))
ax1 = plt.subplot(111)
ax1.plot(sigmawf.time*1e6, sigmawf.amp,'k',label='original')
ax1.plot(sigfiltwf1.time*1e6, sigfiltwf1.amp, label='simple filt < ' + str("%.2g" % f1 + ' Hz'))
ax1.plot(sigfiltwf2.time*1e6, sigfiltwf2.amp,label='simple filt < ' + str("%.2g" % f2 + ' Hz'))
ax1.plot(sigcorrelwf.time*1e6, sigcorrelwf.amp,lw=2,label='adapted filt')

ax1.text(0.95, 0.95, 'snr = ' + str(givensnr) + ', signal length = ' + str("%.2g" % givensiglength) + ' s',
         verticalalignment='top', horizontalalignment='right',
         transform=ax1.transAxes,
         color='red', fontsize=15)
ax1.set_xlabel('time [us]')
ax1.set_ylabel('power [sigma]')
ax1.set_xlim(0,10)
ax1.set_ylim(-5)
plt.legend(bbox_to_anchor=(0.5, 0.8), loc=2)
plt.show()
