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
givensiglength =  50e-9

sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

an =analyse.Analyse(det = det)

sim.producetime()
sim.producenoise()
sim.setpowerenvelope('gauss')
simenvwf = waveform.Waveform(sim.time,sim.powerenvelope, type='envelope')

noise = sim.noise
dirac = utils.wf_dirac(len(noise))
diracwf = waveform.Waveform(sim.time,dirac, type='dirac')
f1 = 1e6
f2 = 4e6
freq = np.fft.rfftfreq(len(sim.time), 1./sim.sampling)
filtered = utils.lowpasshard(dirac,sim.sampling,f1)
filtered2 = utils.lowpasshard(dirac,sim.sampling,f2)
filtadapt = an.crosscorrel(diracwf,simenvwf)

#spec = np.absolute(np.fft.rfft(noise))
specfilt = np.absolute(np.fft.rfft(filtered))
specfilt2 = np.absolute(np.fft.rfft(filtered2))
specfiltadapt = np.absolute(np.fft.rfft(filtadapt.amp))

fig1 = plt.figure(figsize = (8,8))

ax2 = plt.subplot(111)
specfilt = specfilt*specfilt
specfilt2 = specfilt2*specfilt2
specfiltadapt = specfiltadapt*specfiltadapt
ax2.semilogy(freq/1e6, specfilt/np.max(specfilt), label='simple filter f_lim = '+str("%.2g" % f1 + ' Hz'))
ax2.semilogy(freq/1e6, specfilt2/np.max(specfilt2),label='simple filter f_lim = '+str("%.2g" % f2 + ' Hz'))
ax2.semilogy(freq/1e6, specfiltadapt/np.max(specfiltadapt),label='gaussian input #sigma = '+str("%.2g" % givensiglength + ' s'))

ax2.set_xlabel('frequency [MHz]',fontsize=15)
ax2.set_ylabel('gain [a.u.]',fontsize=15)
ax2.set_ylim(1e-35,10)
ax2.set_xlim(0,30)

plt.legend(fontsize=15)
plt.show()
