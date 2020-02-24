import numpy as np
import pandas as pd
from random import shuffle
import scipy, scipy.io
import matplotlib
import matplotlib.pyplot as plt
import os, glob, struct, sys, time, gzip, copy, logging
import math, random, pickle
from tqdm import tqdm
from collections import OrderedDict
from pathlib import Path

from joblib import Parallel, delayed

import matlab.engine
import engine


from pyexperimentparser.experiment.experiment import  Experiment
from pyexperimentparser.trial.trial import Trial
from pyexperimentparser.trial.bda import Bda
from pyexperimentparser.trial.tpa import Tpa


class Dataset:
    def __init__(self, verbosity, cores):
        self.experiment_list = []
        self.dir = ''
        self.cores = cores
        self.verbosity = verbosity    
    
    def mat_to_pkl(self, d, pars):
        print('loading dataset via pickle')
        self.dir = d
        if 'dates_to_process' in pars and len(pars['dates_to_process']) > 0:
            day_dirs = [os.path.join(d,dI) for dI in os.listdir(d) if os.path.isdir(os.path.join(d,dI)) if dI in pars['dates_to_process']]
        else:
            day_dirs = [os.path.join(d,dI) for dI in os.listdir(d) if os.path.isdir(os.path.join(d,dI))]

        #day_dirs = [os.path.join(d,dI) for dI in os.listdir(d) if os.path.isdir(os.path.join(d,dI))]
        idx = 0
        for i, day_dir in enumerate(tqdm(list(day_dirs), desc='collecting dataset...')):
            print("loading %s with pkl protocol %d " % (day_dir, pickle.HIGHEST_PROTOCOL))
            exp_dirs = [os.path.join(day_dir,dI) for dI in os.listdir(day_dir) if os.path.isdir(os.path.join(day_dir,dI))]
            for j, exp_dir in enumerate(exp_dirs):
                if Path(exp_dir + '.pkl').is_file():
                    continue
                    #pass
                else:
                    print('loading', exp_dir)
                experiment = Experiment(idx)
                experiment.load(exp_dir + '/')
                self.experiment_list.append(experiment)
                with open(exp_dir + '.pkl','wb') as f:
                    pickle.dump(experiment, f, pickle.HIGHEST_PROTOCOL)
                idx += 1

    def load_from_pkl_worker(self, i, day_dir, pars):
        ct = "_0"
        if pars['cell_type'] == 'soma':
            ct = "_1"
        else:
            ct = "_2"
        exp_dirs = [os.path.join(day_dir,dI) for dI in os.listdir(day_dir) if (os.path.isdir(os.path.join(day_dir,dI)) 
                                                                            and dI[-2:] == ct)]
        exp_list = []
        for j, exp_dir in enumerate(exp_dirs):
            if Path(exp_dir + '.pkl').is_file():
                exp = Experiment(-1) # temporary instance
                experiment = exp.load_from_pkl(exp_dir + '.pkl')
                exp_list.append(experiment)    
        return exp_list 

    def to_pckl(self):
        with open('./dataset.pkl','wb') as f:
            pickle.dump(self.__dict__, f, pickle.HIGHEST_PROTOCOL)
                
    def load_from_pkl(self, d, pars):
        print('loading dataset from pickle with %d threads, %d verbosity' % (self.cores, self.verbosity))
        self.dir = d
        if 'dates_to_process' in pars and len(pars['dates_to_process']) > 0:
            day_dirs = [os.path.join(d,dI) for dI in os.listdir(d) if os.path.isdir(os.path.join(d,dI)) if dI in pars['dates_to_process']]
        else:
            day_dirs = [os.path.join(d,dI) for dI in os.listdir(d) if os.path.isdir(os.path.join(d,dI))]
        exp_list = Parallel(n_jobs=self.cores, verbose=self.verbosity, backend="threading")(delayed(self.load_from_pkl_worker)(i, day_dir, pars) for i, day_dir in enumerate(list(day_dirs)))
        exp_list = [item for items in exp_list for item in items]
        self.experiment_list = self.experiment_list + exp_list

