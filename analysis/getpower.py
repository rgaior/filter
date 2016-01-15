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

givensnr = 10
givensiglength = 200e-9

sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.setpowerenvelope('gauss')
sim.producesignal()

thesignal = sim.noise + sim.signal

simwf = waveform.Waveform(sim.time,thesignal, type='hf')
wf = det.producesimwaveform(simwf,'adc')

an =analyse.Analyse(det = det)

#get the watt waveform
wattwf = an.producepowerwaveform(wf)

#get the y axis in sigma unit
sigmawf = an.producesigmawaveform(wattwf)

#get the y axis in average unit
meanwf = an.producemeanwaveform(wattwf)


fig1, (ax0, ax1, ax2, ax3) = plt.subplots(4, sharex=True,figsize = (8,8))
fig1.subplots_adjust(hspace=0)
ax =  [ax0, ax1, ax2, ax3]
ax0.plot(1e6*wf.time, wf.amp)
ax0.locator_params(nbins=4)
ax0.set_ylabel('[ADC]',fontsize=15)
ax0.set_title('SNR = '+str(givensnr))

ax1.plot(1e6*wattwf.time,1e6*wattwf.amp)
ax1.locator_params(nbins=4)
ax1.set_ylabel('1e6*P [Watt]',fontsize=15)
ax1.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
ax2.plot(1e6*meanwf.time, meanwf.amp,label=meanwf.type)
ax2.locator_params(nbins=4)
ax2.set_ylabel('[mean]',fontsize=15)
ax3.plot(1e6*sigmawf.time, sigmawf.amp)
ax3.locator_params(nbins=4)
ax3.set_ylabel('[sigma]',fontsize=15)
ax3.set_xlabel('time [us]',fontsize= 15)

plt.legend()
for label in ax0.get_yticklabels():
    print label
plt.show()
