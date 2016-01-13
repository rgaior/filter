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
import waveform
from scipy.optimize import curve_fit

#def func(x, a, mu, sigma):
#    return np.log10(a*np.exp((x - mu)**2)/sigma)
def func(x, a, sigma,mu,b):
    return np.log10((a/sigma)*np.exp(-((x - mu)/sigma)**2)+1e-10) +b

#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)

#givensnr = [1,2,5,10,100]
givensnr = 10
givensiglength = 100e-9
fig1 = plt.figure(figsize = (8,8))
snrafter = np.array([])
sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.setpowerenvelope('gauss')
sim.producesignal()

thesignal = sim.noise + sim.signal
simwf = waveform.Waveform(sim.time,thesignal, type='hf')

wf = det.produceresponse(simwf)
x = wf.time
x = 1e6*x

popt, pcov = curve_fit(func, x, wf.amp, p0=[10*givensnr,0.03,2,-30])
print popt
    
plt.subplot(111)
plt.plot(x,wf.amp)
plt.plot(x,func(x,popt[0],popt[1],popt[2],popt[3]))
plt.show()
