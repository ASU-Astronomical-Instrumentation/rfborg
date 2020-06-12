#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
from PullTouchstoneFiles import pullTouchstone
import scipy.signal as sig
import scipy.stats as stats
import time,os,glob

from scipy import ndimage


# In[36]:


class KID:
    def __init__(self, config_file = "./general_config", Touchstone = False):
        if config_file == "./general_config":
            print("You are using the default config file: general_config.")

        # Pulls parameters from config_file
        gc = np.loadtxt(config_file, dtype = "str") # Loads the user specified general configuration txt file
        self.folderName = np.str(gc[np.where(gc == 'folderName')[0][0]][1]) # pulls user specified folder name where data is stored
        directory = os.path.abspath(self.folderName) # returns absolute path of data folder
        self.samp_freq = np.float(gc[np.where(gc == 'samp_freq')[0][0]][1]) # pulls user specified sample frequency (Hz)
    
        """
        # OS-independent file grabber
        # '__file__' does not work in python shell, need to implement in script
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        print(THIS_FOLDER)
        directory = os.path.join(THIS_FOLDER,filename)
        print(directory)"""
        
        # Extracts I/Q from path
        if Touchstone == True:            
            # Extract from Touchstone file (.S2P/.s2p)
            dataSets = pullTouchstone(directory)
            rawDataSet = rf.Network(dataSets[0]) # Takes the first dataset
            self.I = rawDataSet.s_re[:,1,0]
            self.Q = rawDataSet.s_im[:,1,0]
            unit = rawDataSet.frequency.unit
            self.freq = rawDataSet.frequency.f_scaled
            self.mag = np.sqrt(self.I**2+self.Q**2)
            # Set frequency to MHz
            if unit == 'Hz':
                self.freq = self.freq*1.0e-6
            if unit == 'kHz':
                self.freq = self.freq*1.0e-3
            if unit == 'GHz':
                self.freq = self.freq*1.0e3
            if unit == 'THz':
                self.freq = self.freq*1.0e6
        else:
            I = glob.glob(directory+'/I*.npy')
            Q = glob.glob(directory+'/Q*.npy')
            bb_freqs = glob.glob(directory+'/bb_freqs.npy')
            sweep_freqs = glob.glob(directory+'/sweep_freqs.npy')
            # load array from .npy files
            bb_freqs = np.load(bb_freqs[0])
            sweep_freqs = np.load(sweep_freqs[0])
            
            #Missing two I/Q files, so I'm slicing the sweep_freqs [testing only]
            print('sliced 2 sweep freqs due to 2 missing I/Q files in example folder')
            sweep_freqs = sweep_freqs[2:]
            
            Q = np.array([np.load(filename) for filename in Q])
            I = np.array([np.load(filename) for filename in I])
            self.Q = np.reshape(np.transpose(Q),(len(Q[0])*len(sweep_freqs)))
            self.I = np.reshape(np.transpose(I),(len(I[0])*len(sweep_freqs)))
            mags = np.sqrt(self.I**2+self.Q**2)
            
        
        rf_freqs = np.zeros((len(bb_freqs),len(sweep_freqs)))
        for chan in range(len(bb_freqs)):
            rf_freqs[chan] = (sweep_freqs+bb_freqs[chan])
        rf_freqs = np.hstack(rf_freqs)
        self.freq = np.roll(rf_freqs,int(len(rf_freqs)/2)) # reorder from min to max
        mags = np.roll(mags,int(len(mags)/2)) # recenters dataset
        self.mag = 20*np.log10(mags/np.max(mags))            
        
        #print("BB Frequencies: ")
        #print(bb_freqs)

        # Frequency Comb Parameters
        self.fft_len = 1024 #int(len(self.freq))
        self.LUTbuffer_len = 2**21
        self.dac_freq_res = 2*self.samp_freq/self.LUTbuffer_len
        self.min_neg_freq = np.float(gc[np.where(gc == 'min_neg_freq')[0][0]][1])
        self.max_neg_freq = np.float(gc[np.where(gc == 'max_neg_freq')[0][0]][1])
        self.min_pos_freq = np.float(gc[np.where(gc == 'min_pos_freq')[0][0]][1])
        self.max_pos_freq = np.float(gc[np.where(gc == 'max_pos_freq')[0][0]][1])
        self.symm_offset = np.float(gc[np.where(gc == 'symm_offset')[0][0]][1]) # Offset between positive and negative combs, Hz
        self.Nfreq = np.int(gc[np.where(gc == 'Nfreq')[0][0]][1]) # Number of tones in test comb
        self.freq_comb = np.array([]) # amplitude spectrum of tones
        self.trans_func = np.array([])
        self.tones = np.zeros(self.Nfreq) # frequency tones in comb
        
        
    def plotVNA(self):
        plt.figure()
        plt.plot(self.freq/1.0e6,self.mag)
        plt.title(self.folderName, size = 16)
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Magnitude (dB)')
        plt.grid()
        plt.tight_layout()

    
    def makeFreqComb(self, apply_trans_func = True,Newman = False):
        # Makes an array of N frequencies from minimum negative frequency to maximum positive frequency given in the config file  
        print("Making frequency comb...")
        self.fft_len = int(self.LUTbuffer_len/1024)
        print("FFT_Len"+str(self.fft_len))
        if self.Nfreq == 1:
            print("Choose a frequency between " + str(self.min_pos_freq) + "Hz and " + str(self.max_pos_freq) + " Hz")
            while True:
                try:
                    single_tone = eval(input("Enter single tone frequency in Hz: "))
                    if self.min_pos_freq <= single_tone <= self.max_pos_freq:
                        print("Good")
                        break
                except ValueError:
                    print("Invalid number. Commencing self-destruct sequence!")
            self.tones = single_tone
        else:
            neg_freqs, neg_delta = np.linspace(self.min_neg_freq + self.symm_offset, self.max_neg_freq + self.symm_offset, int(self.Nfreq/2), retstep = True)
            pos_freqs, pos_delta = np.linspace(self.min_pos_freq, self.max_pos_freq, int(self.Nfreq/2), retstep = True)
            self.tones = np.concatenate((neg_freqs,pos_freqs))
        k = self.fft_bin_index()
        freq_comb = np.zeros(self.fft_len)
        if apply_trans_func == True:
            print("Applying transfer function...")
            # Load transfer function from file (To Be Done At A Later Time)

            # Generate transfer function
            self.get_transfunc()
            amp = self.trans_func
            print("Done!")
        else:
            amp = 1.0
        for toneNumber,binIndex in enumerate(k):
            if Newman == True:
                    phase = np.pi*(self.tones[toneNumber]-1)**2/Nfreq
                    freq_comb[binIndex] = amp[toneNumber]*np.exp(1.0j*phase)
            else:
                phase = np.random.uniform(0,2*np.pi)
                freq_comb[binIndex] = amp[toneNumber]*np.exp(1.0j*phase)
        #freq_comb = freq_comb[freq_comb != 0]
        if len(freq_comb) == 0:
            raise ValueError("Frequency comb empty!")
        #freq_comb = np.roll(freq_comb, - np.argmin(np.abs(freq_comb)) - 1) # Rolls/shifts elements by a specified amount in an array
        print("Write comb to some register")
        self.freq_comb = freq_comb
        print("Done!")

    def fft_bin_index(self):
    # returns the fft bin index for a given frequency, fft length, and sample frequency
        k = np.round((self.tones/self.samp_freq)*self.fft_len).astype('int')
        k = np.array([k])
        return k

    def plotFreqComb(self):
        freqs = np.linspace(0,self.samp_freq,self.fft_len)#np.linspace(self.min_pos_freq,self.max_pos_freq,self.fft_len)
        plt.figure()
        plt.plot(freqs*1.0e-6,self.freq_comb,'.')
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Tone Amplitude")
        plt.grid()
        plt.tight_layout()
        
    def plotWaveform(self):
        waveform = np.fft.ifft(self.freq_comb)
        time = np.linspace(0,2./self.samp_freq,len(waveform))
        plt.figure()
        plt.plot(time*1.0e9,waveform)
        plt.xlabel("Time (ns)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.tight_layout()
        
    def get_transfunc(self):
        # Take N=100 samples from BRAM and find the mean in each bin associated with the frequency comb. 
        # Normalize the means to the maximum mean value giving a 1 at the frequency where the power is largest else less than 1.
        # Take the inverse so the frequency with largest power is unchanged and the rest are increased.
        # This is the transfer function 
        print("Calculating transfer function...")
        mag_array = np.zeros((100, int(self.Nfreq)))
        for i in range(100):
            I, Q = self.I + np.random.normal(0,0.1),self.Q + np.random.normal(0,0.1) #Gaussian noise was added for simulation; self.read_accum_snap()
            mags = np.sqrt(I**2 + Q**2)
            mag_array[i] = mags[0:int(self.Nfreq)] # mags[2:len(self.freq_comb)+2]
        mean = np.mean(mag_array, axis = 0)
        transfunc = 1./ (mean / np.max(mean))
        self.trans_func = transfunc
        #np.save('./last_transfunc.npy', transfunc)
        print("Done!")
        return
    
    def fitFreqs(self,peak_threshold, debugging = False):
        freqs = self.freq
        I = self.I
        Q = self.Q
        mags = self.mag
        filtered = self.savgol()
        
        if debugging:
            plt.figure()
            #plt.clf() # clears figure
            plt.plot(freqs,mags,label = 'Raw')
            plt.plot(freqs,filtered,label = 'Smoothed')
            plt.xlabel('frequency [MHz]', fontsize = 16)
            plt.ylabel('|S21| [dB]', fontsize = 16)
            plt.legend()
            plt.tight_layout()
            
            plt.figure()
            #plt.clf()
            plt.plot(freqs,mags-filtered, label = 'TRF corrected')
            plt.xlabel('frequency [MHz]', fontsize = 16)
            plt.ylabel('|S21| dB', fontsize = 16)
            plt.legend()
            plt.tight_layout()
            
        iup = np.where( (mags-filtered) > -1.0*peak_threshold)[0]
        new_mags = mags - filtered
        new_mags[iup] = 0
        labeled_image, num_objects = ndimage.label(new_mags)
        indices = ndimage.measurements.minimum_position(new_mags,labeled_image,np.arange(num_objects)+1)
        kid_idx = np.array(indices).ravel()
        if len(kid_idx) == 0:
            print('No KIDs below this peak threshold')
        else:
            print(len(kid_idx), 'KIDs Found!')
        #freqs[kid_idx]
        
    def findRes(self):
        peaks, __ = sig.find_peaks(-self.mag,prominence=(10.0,None))
        resFreq = self.freq[peaks] # Hz
        return resFreq
    
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
        return sig.savgol_filter(self.mag,window,poly,mode=mode)
        
class TES:
    def __init__(self):
        print("Your outdated detector technology is unacceptable. You will be assimilated...")


# In[37]:


obj1 = KID()
obj1.makeFreqComb()
a = obj1.freq_comb
obj1.plotFreqComb()
#obj1.plotWaveform()


# ![Futile](https://media.giphy.com/media/twSrnNsCC4z60/giphy.gif "borg")

# In[ ]:




