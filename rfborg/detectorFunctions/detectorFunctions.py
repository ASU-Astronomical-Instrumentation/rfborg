import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
from PullTouchstoneFiles import pullTouchstone
import scipy.signal as sig
import scipy.stats as stats


class KID:
    def __init__(self, config_file = "./general_config"):
        if config_file == "./general_config":
            print("You are using the default config file: general_config.")

        # Pulls parameters from config_file
        gc = np.loadtxt(config_file, dtype = "str")
        folderpath = np.str(gc[np.where(gc == 'folderpath')[0][0]][1])  # Pull from BRAM or stored file
        # Extracts I/Q from path
        dataSets = pullTouchstone(folderpath)
        rawDataSet = rf.Network(dataSets[0]) # Takes the first dataset
        self.I = rawDataSet.s_re[:,1,0]
        self.Q = rawDataSet.s_im[:,1,0]
        self.freq = rawDataSet.frequency.f_scaled
        self.mag = np.sqrt(self.I**2+self.Q**2)
        
    # Plots magnitude
    def plot(self):
        plt.figure()
        plt.plot(self.freq,self.mag)
        
    def findRes(self):
        peaks, __ = sig.find_peaks(-self.mag,prominence=(0.5,None))
        resFreq = self.freq[peaks] # Hz
        print(resFreq)
    
    # Apply Savitsky-Golay filter
    def savgol(self):
        window_length = len(self.mag)/25
        if (window_length)%2 == 0:
            window = window_length +1
        else:
            window = window_length
        poly = 2
        #modes = ['interp','mirror','nearest','constant','wrap']
        mode = 'wrap'
        self.mag = sig.savgol_filter(self.mag,window,poly,mode=mode)
        
class TES:
    def __init__(self):
        print("Your outdated detector technology is unacceptable. You will be assimilated...")