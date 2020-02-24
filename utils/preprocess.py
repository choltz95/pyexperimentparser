import sys
sys.path.insert(0,'../submodule/')
sys.path.insert(0,'../submodule/OASIS')
sys.path.insert(0,'../submodule/OASIS/oasis')


from tqdm import tqdm
import numpy as np
"""
from oasis.functions import gen_data, gen_sinusoidal_data, deconvolve, estimate_parameters
from oasis.plotting import simpleaxis
from oasis.oasis_methods import oasisAR1, oasisAR2


def deconvolve(spikes):
  train_data_norma = []
  valid_data_norma = []
  train_data_spikes = []
  valid_data_spikes = []
  for i in tqdm(range(spikes.shape[0])):
      cs = []
      ss = []
      bs = []
      gs = []
      lams = []
      for y in spikes[i].T:
        c, s, b, g, lam = deconvolve(y.astype(np.double), g=(None,None), penalty=1) 
        cs.append(c)
        ss.append(s)
        bs.append(b)
        gs.append(g)
        lams.append(lam)
      denoised = (bs + np.array(cs).T)
      train_data_norma.append(denoised)
      train_data_spikes.append(np.array(ss))

  spikes = np.array(spikes)

  return spikes
"""

def z_normalize(X):
    X = X - np.mean(X, axis=0)[None, :, :]
    std = np.std(X, axis=0)[None, :, :]
    X = X / np.where(std > 0, std, 1)
    return X

def max_normalize(X,ax=0):
    minX = np.repeat(np.min(X, axis=ax)[ np.newaxis, :, :],X.shape[ax],ax)
    maxX = np.repeat(np.max(X, axis=ax)[ np.newaxis, :, :],X.shape[ax],ax)
    denom = (maxX - minX)
    X = (X - minX) / np.where(denom > 0, denom, 1)
    return X

def mean_center(X,ax=0):
    X = X - np.mean(X, axis=0)[None, :, :]
    return X