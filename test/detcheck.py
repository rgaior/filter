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
from scipy.optimize import curve_fit

def func(x, a, sigma,mu,b):
    return np.log10((a/sigma)*np.exp(-((x - mu)/sigma)**2)+1e-10) + b

#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)

givensnr = [1,2, 10, 50, 100]
#givensnr = [10,100]
givensiglength = 100e-9
fig1 = plt.figure(figsize = (8,8))
snrafter = np.array([])
for snr in givensnr:
    sim = simulation.Simulation(det=det, snr=snr, siglength = givensiglength)

    sim.producetime()
    sim.producenoise()
    sim.producesignal()

    thesignal = sim.noise + sim.signal
    
    wf = det.produceresponse(thesignal)
    x = np.linspace(0, float(len(wf))/sim.sampling, len(wf))
    x = 1e6*x
    popt, pcov = curve_fit(func, x, wf, p0=[0.1,0.03,2,-30])
    fitted = func(x,popt[0],popt[1],popt[2],popt[3])
    noiseafter = np.mean(fitted[len(fitted)/2:])
    sigafter = np.max(fitted)
    print 'noise after = ', noiseafter
    print 'max = ', sigafter
    snrafter = np.append(snrafter,sigafter - noiseafter)
    plt.subplot(111)
    plt.plot(x,wf, label='snr = ' +str(snr))
    plt.plot(x,fitted,'k',lw=2 )
    plt.xlim(0,5)
    plt.xlabel('time [us]')
    plt.ylabel('power [dBm]')
    
plt.legend()
mean = np.mean(wf)
std = np.std(wf)

fig2 = plt.figure()
ax1 = plt.subplot(111)
ax1.plot(np.asarray(givensnr), (np.power(10,snrafter/10)-1) - np.asarray(givensnr),'o')
ax1.set_xlabel('input SNR')
ax1.set_ylabel('output SNR - input SNR')
#n1, bins1, patches1 = ax1.hist(wf, 50, facecolor='red', alpha=0.75)
#ax1.text(0.95, 0.90, 'mean = ' + str(mean) + '\n' + 'std = '+ str(std),
 #       verticalalignment='bottom', horizontalalignment='right',
 #       transform=ax1.transAxes,
  #      color='black', fontsize=15)

plt.show()
