import numpy as np
import pandas as pd
from random import shuffle
import scipy
import scipy.io
import matplotlib
import matplotlib.pyplot as plt
from importlib import import_module
import os, json, glob, struct, sys, time, gzip, copy, logging
import math, random, pickle
from tqdm import tqdm
from collections import OrderedDict
from pathlib import Path
from sys import path
path.append('matlab')

from joblib import Parallel, delayed

import matlab.engine
import engine

from pyexperimentparser.dataset.dataset import  Dataset
from pyexperimentparser.experiment.experiment import  Experiment
from pyexperimentparser.trial.trial import Trial
from pyexperimentparser.trial.bda import Bda
from pyexperimentparser.trial.tpa import Tpa

from importlib import import_module

from absl import app
from absl import logging
from absl import flags

FLAGS = flags.FLAGS


flags.DEFINE_string('config_filename', 'config.json', 'config filename')
flags.DEFINE_string('dir', 'out', 'output directory')
flags.DEFINE_string('data_filename', 'data.out', 'filename for generated data')
flags.DEFINE_boolean('debug', False, 'output runtime debug info')
flags.DEFINE_boolean('novar', False, 'do not show std in the output figure')
flags.DEFINE_boolean('rm', False, 'remove previously generated data')
flags.DEFINE_boolean('fig', False, 'generate figure only')

DATASET_PKG = 'pyexperimentparser.dataset'
EXPERIMENT_PKG = 'pyexperimentparser.experiment'
TRIAL_PKG = 'pyexperimentparser.trial'

def parse(config):
  pars = config['parameters']
  return pars

def main(argv):
  del argv
  engine.init()

  if FLAGS.debug:
    # DEBUG, INFO, WARN, ERROR, FATAL
    logging.set_verbosity(logging.DEBUG)
  else:
    logging.set_verbosity(logging.INFO)

  data_file = os.path.join(FLAGS.dir, FLAGS.data_filename)

  # load config
  with open(FLAGS.config_filename, 'r') as json_file:
    config = json.load(json_file)

  if not FLAGS.fig:
    pars = parse(config)

    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    prev_files = os.listdir(FLAGS.dir)
    if FLAGS.rm:
      for file in prev_files:
        os.remove(os.path.join(FLAGS.dir, file))
    else:
      if os.listdir(FLAGS.dir):
        logging.fatal(('%s/ is not empty. Make sure you have'
                       ' archived previously generated data. '
                       'Try --rm flag which will automatically'
                       ' delete previous data.') % FLAGS.dir)

    trial_ind_show = 0
    data_dir = pars['data_dir']
    # special trial (repetition) to show (Change it if you need)
    rois_per_trial_num = pars['rois_per_trial_num']
    # frame rate ratio between Two Photon imaging and Behavior
    frame_rate_ratio      = pars['frame_rate_ratio']
    # Common names to be converted to Ids
    event_name_list      = pars['event_name_list']

    procs = pars['processors']
    verbosity = pars['verbosity']

    ds = Dataset(verbosity, procs)
    #ds.mat_to_pkl(data_dir)
    ds.load_from_pkl(data_dir)
    ds.to_pckl()
    
    Data_x = []
    Data_y = []
    for exp in tqdm(ds.experiment_list):
        for trial in exp.trial_list: 
            if len(trial.bda_list) < 1 or len(trial.tpa_list) < 1:
                continue

            #trial.tpa_list[-1].print_param()
            #trial.bda_list[-1].print_param()

            rois_per_trial_num   = len(trial.tpa_list)
            dffData = trial.tpa_list[0].procROI
            framNum = dffData.shape[0]
            dffDataArray = np.tile(dffData, (rois_per_trial_num,1))
            roiNames = []

            for m in range(rois_per_trial_num):
                dffDataArray[m,:] = trial.tpa_list[m].procROI
                roiNames.append(trial.tpa_list[m].Name)
                
            # extract ROI df/F data
            rois_per_trial_num   = len(trial.tpa_list)
            dffData = trial.tpa_list[0].procROI
            framNum = dffData.shape[0]
            dffDataArray = np.tile(dffData, (rois_per_trial_num,1))
            roiNames = []

            for m in range(rois_per_trial_num):
                dffDataArray[m,:] = trial.tpa_list[m].procROI
                roiNames.append(trial.tpa_list[m].Name)
                       
            # extract Event Time data
            eventsPerTrialNum   = len(trial.bda_list)
            timeData         = trial.bda_list[0].TimeInd
            eventDataArray   = np.zeros((framNum,eventsPerTrialNum))
            eventNames       = []

            for m in range(eventsPerTrialNum):
                timeInd     = np.array(trial.bda_list[m].tInd).flatten()
                timeInd     = np.round(timeInd/frame_rate_ratio) # transfers to time of the two photon

                timeInd     = np.concatenate(([1],[np.min(np.concatenate((timeInd, [framNum])))]))
                timeInd = np.sort(timeInd)
                eventDataArray[int(timeInd[0]):int(timeInd[1]),m] = 1
                eventNames.append((trial.bda_list[m].Name, trial.bda_list[m].SeqNum))
           
            if len(eventNames) > 1:
                Data_x.append(dffDataArray.T)
                if eventNames[1][0] == 'success':
                    Data_y.append(1)
                else:
                    Data_y.append(0)

    Data_x_subset = []
    Data_y_subset = []
    for i, x in enumerate(Data_x):
        if x.shape[-1] == 379 and x.shape[0] == 360:
            Data_x_subset.append(x)
            Data_y_subset.append(Data_y[i])

    #np.save(open('X.out','bw'), np.stack(Data_x_subset))
    #np.save(open('y.out','bw'), np.array(Data_y_subset))

if __name__ == '__main__':
  app.run(main)
