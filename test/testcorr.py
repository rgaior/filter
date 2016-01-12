from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
cwd = os.getcwd()
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
import utils

x = np.linspace(0,5e-6,10000)
sig = utils.func_normedgauss(x,2.5e-6,50e-9)
intsig = np.sum(sig)
sigma = 3
sig_noise = sig + sigma*np.random.randn(len(sig))

corr = signal.correlate(sig_noise, sig, mode='same')/intsig
#xcorr = np.linspace(len(corr))

plt.subplot(211)
plt.plot(x,sig_noise)
plt.plot(x,sig,'k')


plt.subplot(212)
plt.plot(x, corr)
plt.show()
