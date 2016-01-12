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
from scipy.optimize import curve_fit

def func(x, a, sigma,mu,b):
    return np.log10((a/sigma)*np.exp(-((x - mu)/sigma)**2)+1e-10) + b

nrofsample = 20
#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)

#givensnr = [1,2, 10, 50, 100]
givensnr = [1,2,10,50,100]
snrtable = np.ndarray(shape = (len(givensnr),nrofsample ), dtype=float)
givensiglength = 100e-9
fig1 = plt.figure(figsize = (8,8))
snrafter = np.array([])
countersnr = 0
for snr in givensnr:
    for s in range(nrofsample):
        sim = simulation.Simulation(det=det, snr=snr, siglength = givensiglength)
        
        sim.producetime()
        sim.producenoise()
        sim.producesignal()

        thesignal = sim.noise + sim.signal
    
        wf = det.produceresponse(thesignal)
        x = np.linspace(0, float(len(wf))/sim.sampling, len(wf))
        x = 1e6*x
        popt, pcov = curve_fit(func, x, wf, p0=[10*snr,0.03,2,-25])
        fitted = func(x,popt[0],popt[1],popt[2],popt[3])
        noiseafter = np.mean(fitted[len(fitted)/2:])
        sigafter = np.max(fitted)
#        print 'input snr = ', snr, 'output snr = ', np.power(10,(sigafter-noiseafter)/10)-1
        snrtable[countersnr][s] = np.power(10,(sigafter-noiseafter)/10)-1
    countersnr +=1 

#plotting:
for snrcount in range(len(givensnr)):
    inpsnr = givensnr[snrcount]
    meanoutsnr = np.mean(snrtable[snrcount])
    fakex = inpsnr*np.ones(len(snrtable[snrcount]))
    plt.xlabel('input SNR',fontsize=15)
    plt.ylabel('(output SNR - input SNR)/ input SNR',fontsize=15)
    plt.xlim(givensnr[0]-0.1*givensnr[0], givensnr[-1]+0.1*givensnr[-1])
    plt.semilogx(fakex,(snrtable[snrcount]-inpsnr)/inpsnr,'o')

plt.show()
