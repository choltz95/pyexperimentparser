import os, glob, logging
import pickle

import os
from pathlib import Path

import engine
try:
    import matlab.engine
except:
    pass

from pyexperimentparser.trial import trial
from pyexperimentparser.trial import Bda
from pyexperimentparser.trial import Tpa
from pyexperimentparser.utils import *


class Experiment:
    """ Experiment

    Parameters
    ----------
    idx : int
        experiment index
    path : string
        path to experiment directory/pickle file.
    ftype : {'pickle', 'mat'}
    (default: pickle)
        types of files to load

    Notes
    -----

    Examples
    -----
    """


    def __init__(self, idx, path='', ftype="pickle"):
        assert ftype in ["pickle","mat"], \
            "ftype needs to be one of: mat, pickle"
        self.ftype = ftype
        self.path = path
        if ftype == "pickle":
            assert Path(self.path).is_file(), \
                "file does not exist!"
            self.filename = os.path.basename(self.path)
            self.directory = os.path.dirname(self.path)
        else:
            assert Path(self.path).is_dir(), \
                "directory does not exist!"
            self.directory = self.path
            self.tpa_fname_list = [fpath for fpath in glob.glob(self.directory + "TPA*")]
            self.bda_fname_list = [fpath for fpath in glob.glob(self.directory + "BDA*")]

        self.trial_list = []
        self.dataset_index = idx

        # comment the format 
        self.day_index = str(self.directory).split('/')[-2].split('_')[-1]
        self.date = str(self.directory).split('/')[-2].split('_')[0]

        self.load()

    def load(self):
        """top-level load fn"""
        if self.ftype == "pickle":
            self._deserialize_from_pickle()
        elif self.ftype == "mat":
            self._deserialize_from_mat()

    def _deserialize_from_mat(self):
        """load from matlab files"""
        for bda_fname, tpa_fname in zip(self.bda_fname_list, self.tpa_fname_list):
            try:
                idx = int(bda_fname.split('/')[-1].split('_')[4])
                tr = trial.Trial(idx, bda_fname, tpa_fname)
                self.trial_list.append(tr)
            except Exception as e:
                print("Error (exp):", bda_fname, " ", tpa_fname)
                print(str(e))
                continue

        # sort trials by day
        self.trial_list = sorted(self.trial_list, key=lambda x: x.idx)

    def _deserialize_from_pickle(self):
        """load from pickle"""
        f = open(self.path, 'rb')
        tmp_dict = pickle.load(f)
        f.close()          
        self.__dict__.update(tmp_dict) 

    def _serialize_to_pickle(self):
        """save self to pickle"""
        f = open(self.path.rstrip('/')  + '.pkl', 'wb')
        pickle.dump(self.__dict__, f, pickle.HIGHEST_PROTOCOL)
        f.close()
