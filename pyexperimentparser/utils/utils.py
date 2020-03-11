import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os, glob, logging
import pickle
from tqdm import tqdm_notebook as tqdm
from pathlib import Path

from pyexperimentparser.dataset import dataset
from pyexperimentparser.experiment import experiment
from pyexperimentparser.trial import trial
from pyexperimentparser.trial import Bda
from pyexperimentparser.trial import Tpa

def save_npy(np, fpath):
  """save npy if path exists"""
  pass

def load_obj_from_pkl(fileName):
  """load object from pickle if path exists"""
  # assert path exists
  f = open(fileName,"rb")
  obj = pickle.load(f)
  f.close()
  return obj

def parse_config(confpath):
  """parse json config"""
  with open(confpath, 'r') as json_file:
    config = json.load(json_file)
  return config

def get_cell_type_from_filename(fname):
  """get cell-type from file name"""
  assert type(fname) is StringType, "fname is not a string: %r" % name
  tag = fname[-6:-4]
  if tag == "_1":
    return "s"
  elif tag == "_2":
    return "d"
  else:
    print('[ERR] unkown cell-type ' + fname)
    return ''

def get_day_directories_from_path(dir, days=[]):
  """get experiment directories corresponding to dates"""
  if len(days) > 0:
    return [os.path.join(d,dI) for dI in os.listdir(d) if os.path.isdir(os.path.join(d,dI)) if dI in days]
  else: 
    return [os.path.join(d,dI) for dI in os.listdir(d) if os.path.isdir(os.path.join(d,dI))]

def serialize_experiments():
  """convert experiment tpa/bda files to serialized experiments"""
  day_dirs = utils.get_day_directories_from_path(self.datadir, self.dates_to_process)
  for i, day_dir in enumerate(tqdm(list(day_dirs), desc='collecting dataset...')):
      print("loading %s with pkl protocol %d " % (day_dir, pickle.HIGHEST_PROTOCOL))
      exp_dirs = [os.path.join(day_dir,dI) for dI in os.listdir(day_dir) 
                  if os.path.isdir(os.path.join(day_dir,dI))]
      for j, exp_dir in enumerate(exp_dirs):
          experiment = Experiment(i, exp_dir)
          experiment.save_pickle()