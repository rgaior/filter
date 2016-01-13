import numpy as np
import os
import sys
#plotting
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
#include the needed paths
cwd = os.getcwd()
classpath = cwd + '/../classes/'
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
sys.path.append(classpath)
#my stuff
import utils
import simulation
import detector
import waveform

#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
bw= 8e8
tau = 5e-9
det = detector.Detector(tsys, gain, bw,tau)

givensnr = 10
givensiglength = 500e-9
sim = simulation.Simulation(det=det, snr=givensnr, siglength = givensiglength)

sim.producetime()
sim.producenoise()
sim.producesignal()

thesignal = sim.noise + sim.signal

simwf = waveform.Waveform(sim.time,thesignal, type='hf')

#fig1 = plt.figure(figsize = (8,8))
#ax1 = plt.subplot(111)
#ax1.plot(wf[0], wf[1],label='signal after adapt. board')

#plt.legend()
#plt.show()
