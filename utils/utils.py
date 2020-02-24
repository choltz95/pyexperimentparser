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

from pyexperimentparser.dataset import dataset
from pyexperimentparser.experiment import Experiment
from pyexperimentparser.trial import trial
from pyexperimentparser.trial import bda
from pyexperimentparser.trial import tpa

def save_npy(np, fpath):
  if path.exists(fpath):
    print('path exists!')
    return 1
  if type(np) is not np.ndarray:
    print('variable is not numpy array!')
    return 1

  with open(fpath,'wb') as f:
    np.save(fpath, np)
