import numpy as np
import pandas as pd
from random import shuffle
import scipy
import scipy.io
import matplotlib
import matplotlib.pyplot as plt
import os, glob, struct, sys, time, gzip, copy, logging
import math, random
import pickle
from tqdm import tqdm
from collections import OrderedDict
from pathlib import Path

from joblib import Parallel, delayed

import matlab.engine
import engine


from pyexperimentparser.trial import bda
from pyexperimentparser.trial import tpa


class Trial:
    def __init__(self, idx):
        self.bda_list = []
        self.tpa_list = []
        self.bda_fname = ''
        self.tpa_fname = ''
        self.date = ''
        self.idx = idx
        
    def load_bdas_tpas(self, bda_fname, tpa_fname):
        self.bda_fname = bda_fname
        self.tpa_fname = tpa_fname
        
        strROIs = engine.eng.load(tpa_fname)['strROI']
        strShifts = engine.eng.load(tpa_fname)['strShift']

        for i, strROI in enumerate(strROIs):
            try:
                tmp_tpa = tpa.Tpa()
                if i < len(strShifts):
                    strShift = strShifts[i]
                else:
                    strShift = None
                tmp_tpa.load(strROI, strShift)
                self.tpa_list.append(tmp_tpa)
            except Exception as e:
                print("Error (strROI):", bda_fname, " ", tpa_fname)
                print(str(e))
                continue  
            
        strEvents = engine.eng.load(bda_fname)['strEvent']
        for strEvent in strEvents:  
            try:
                tmp_bda = bda.Bda()
                tmp_bda.load(strEvent)
                self.bda_list.append(tmp_bda)
            except Exception as e:
                print("Error (strEvents):", bda_fname, " ", tpa_fname)
                print(str(e))
                continue  
            

    def plot(self):
        pass
