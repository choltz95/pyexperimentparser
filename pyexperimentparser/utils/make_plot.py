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
from tqdm import tqdm_notebook as tqdm
from collections import OrderedDict
from pathlib import Path

from joblib import Parallel, delayed

import matlab.engine
import engine


from pyexperimentparser.dataset import dataset
from pyexperimentparser.experiment import Experiment
from pyexperimentparser.trial import trial
from pyexperimentparser.trial import bda
from pyexperimentparser.trial import tpa

def make_plot():
    Data_dir = './data/'

    # special trial (repetition) to show (Change it if you need)
    trialIndShow        = 0
    roisPerTrialNum = 1
    # frame rate ratio between Two Photon imaging and Behavior
    frameRateRatio      = 6*3 # (do not touch)
    # Common names to be converted to Ids
    eventNameList      = {'Lift','Grab','Sup','Atmouth','Chew','Sniff','Handopen','Botharm','Tone','Table'} # (do not touch)
    cores = -1
    verbosity = 10

    dataset = dataset.Dataset(verbosity, cores)
    dataset.load_from_pkl(Data_dir)

    # extract ROI df/F data
    Trial_tst = dataset.experiment_list[0].trial_list[trialIndShow]

    roisPerTrialNum   = len(Trial_tst.tpa_list)
    dffData = Trial_tst.tpa_list[0].procROI
    framNum = dffData.shape[0]
    dffDataArray = np.tile(dffData, (roisPerTrialNum,1))
    roiNames = []

    for m in range(roisPerTrialNum):
        dffDataArray[m,:] = Trial_tst.tpa_list[m].procROI
        roiNames.append(Trial_tst.tpa_list[m].Name)

    for experiment in dataset.experiment_list:
        for trial in experiment.trial_list:
            for bda in trial.bda_list:
                timeInd     = np.array(bda.tInd).flatten()
                timeInd     = np.round(timeInd/frameRateRatio) # transfers to time of the two photon

                timeInd     = np.concatenate(([1],[np.min(np.concatenate((timeInd, [framNum])))]))
                timeInd = np.sort(timeInd)

    # extract Event Time data
    eventsPerTrialNum   = len(Trial_tst.bda_list)
    timeData         = Trial_tst.bda_list[0].TimeInd
    eventDataArray   = np.zeros((framNum,eventsPerTrialNum))
    eventNames       = []

    for m in range(eventsPerTrialNum):
        timeInd     = np.array(Trial_tst.bda_list[m].tInd).flatten()
        timeInd     = np.round(timeInd/frameRateRatio) # transfers to time of the two photon
        
        timeInd     = np.concatenate(([1],[np.min(np.concatenate((timeInd, [framNum])))]))
        timeInd = np.sort(timeInd)
        eventDataArray[int(timeInd[0]):int(timeInd[1]),m] = 1
        eventNames.append((Trial_tst.bda_list[m].Name, Trial_tst.bda_list[m].SeqNum))
    print(eventNames)

    # plot
    plt.clf()
    plt.figure(figsize=(15, 10))

    ax1=plt.subplot(2, 2, 1)
    timeImage = range(framNum)
    ax1.plot(timeImage, dffDataArray.T) # , label = 'test'
    ax1.legend()
    ax1.set_xlabel('Time [Frame]')
    ax1.set_ylabel('dF/F')
    ax1.set_title('Two Photon data for trial: '+ str(trialIndShow))

    ax2 = plt.subplot(2,2,2)
    ax2.plot(timeImage, eventDataArray, label=eventNames)
    ax2.set_xlabel('Time [Frame]')
    ax2.set_ylabel('Events')
    ax2.set_title('Event duration data for trial: ' + str(trialIndShow))
    ax2.legend()

    ax3 = plt.subplot(2,2,3)

    ax3.imshow(dffDataArray, aspect='auto')

    ax4 = plt.subplot(2,2,4)
    ax4.imshow(eventDataArray, aspect='auto')

    plt.savefig('trial_' + str(trialIndShow))
