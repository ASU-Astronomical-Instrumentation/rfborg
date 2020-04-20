
# coding: utf-8

# In[5]:

import os
import numpy as np


# In[6]:

def pullTouchstone(folderpath):
    directory = folderpath
    dataArray = np.array([])
    for filename in os.listdir(directory): 
        if filename.endswith(".s2p"): # R&S VNA
            dataArray = np.append(dataArray,os.path.join(directory,filename))
            continue
        elif filename.endswith(".S2P"): # Agilent VNA
            dataArray = np.append(dataArray,os.path.join(directory,filename))
            continue
        else:
            continue
    return dataArray

