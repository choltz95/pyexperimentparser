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

import os
from joblib import Parallel, delayed

import matlab.engine
import engine


from pyexperimentparser.trial import trial
from pyexperimentparser.trial import bda
from pyexperimentparser.trial import tpa

class Experiment:
    def __init__(self, idx):
        self.trial_list = []
        self.idx = idx # overall id 
        self.iddx = 0 # day id 
        self.dir = ''
        self.date = ''
        #self.eventNameList = ['Lift','Grab','Sup','Atmouth','Chew','Sniff','Handopen','Botharm', 'Tone','Table','Failure','Success', 'Trying','failure+1','success+1','nopellet', 'Lick', 'Regular', 'sucrose','Quinine', 'Sucrose S','Sucrose F' 'BackToPerch', 'Failure Perch' 'Success Perch' 'T-Failure','P-Failure' 'T-Success' 'P-Success', 'MouthFront' 'Perch' 'Reach' 'Attable','MovmentSuccess','LickAttempt']
        self.eventNameList = ['Lift','Grab','Sup','Atmouth','Chew','Sniff','Handopen','Botharm','Tone','Table']
        
    def l(self, bda_fname, tpa_fname):
        idx = int(bda_fname.split('/')[-1].split('_')[4])
        tmp_trial = trial.Trial(idx)
        tmp_trial.load_bdas_tpas(bda_fname, tpa_fname)
        return tmp_trial
        
    def load(self, d):
        self.iddx = d.split('/')[-2].split('_')[-1]
        self.dir = d
        self.date = d.split('/')[-2].split('_')[0]
        tpa_fname_list = [fpath for fpath in glob.glob(d + "TPA*")]
        bda_fname_list = [fpath for fpath in glob.glob(d + "BDA*")]
        
        for bda_fname, tpa_fname in zip(bda_fname_list, tpa_fname_list):
            try:
                idx = int(bda_fname.split('/')[-1].split('_')[4])
                tmp_trial = trial.Trial(idx)
                tmp_trial.load_bdas_tpas(bda_fname, tpa_fname)
                self.trial_list.append(tmp_trial)
            except Exception as e:
                print("Error (exp):", bda_fname, " ", tpa_fname)
                print(str(e))
                continue
        
        #self.trial_list = Parallel(n_jobs=-1, verbose=0, backend="threading")(delayed(self.l)(bda_fname, tpa_fname) for bda_fname, tpa_fname in zip(bda_fname_list, tpa_fname_list))
        
        # sort trial list by idxs
        self.trial_list = sorted(self.trial_list, key=lambda x: x.idx)

    def load_from_pkl(self, fileName):
        """Return a thing loaded from a file."""
        f = open(fileName,"rb")
        obj = pickle.load(f)
        f.close()
        return obj
