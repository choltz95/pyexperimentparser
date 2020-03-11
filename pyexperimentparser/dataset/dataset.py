import os, glob, logging, pickle
from pathlib import Path
from tqdm import tqdm
from joblib import Parallel, delayed

import engine
try:
    import matlab.engine
except:
    pass

from pyexperimentparser.experiment.experiment import  Experiment
from pyexperimentparser.trial.trial import Trial
from pyexperimentparser.trial.bda import Bda
from pyexperimentparser.trial.tpa import Tpa
from pyexperimentparser.utils import utils


class Dataset:
    """ Dataset

    Parameters
    ----------
    data_dir : string
        data directory
    verbosity : int (default: 5)
        Joblib verbosty.
    cores : int (default: 2)
        # Joblib cores
    ftype : {'pickle', 'mat'}
    (default: pickle)
        types of files to load
    pars : {}

    Notes
    -----

    Examples
    --------
    """


    def __init__(self, data_dir, verbosity=5, cores=2, ftype="pickle", pars={}):
        assert ftype in ["pickle","mat"], \
            "ftype needs to be one of: mat, pickle"
        assert Path(data_dir).is_file(), \
            "directory does not exist!"

        self.experiment_list = []
        self.cores = cores
        self.verbosity = verbosity
        self.ftype = ftype
        self.cell_types = pars['cell_type']
        self.datadir = data_dir
        self.dates_to_process = pars['dates_to_process']

        self.directories_by_day

        self.load()

    def load(self):
        """top-level load fn"""
        if self.ftype == "pickle":
            self._deserialize_experiments_from_pickle()
        elif self.ftype == "mat":
            self._deserialize_experiments_from_mat()

    def _deserialize_experiments_from_mat(self, pars):
      """load from experiments matlab files"""
      day_dirs = utils.get_day_directories_from_path(self.datadir, self.dates_to_process)
      for i, day_dir in enumerate(tqdm(list(day_dirs), desc='collecting dataset...')):
          print("loading %s with pkl protocol %d " % (day_dir, pickle.HIGHEST_PROTOCOL))
          experiment_dirs = [os.path.join(day_dir,dI) for dI in os.listdir(day_dir) 
                             if os.path.isdir(os.path.join(day_dir,dI))]
          for j, exp_dir in enumerate(experiment_dirs):
              experiment = Experiment(i, exp_dir)
              self.experiment_list.append(experiment)

    def __deserialize_experiments_from_mat_worker(self):
        """worker fn for mat deserialize"""
        pass

    def _deserialize_experiments_from_pickle(self, pars):
        """load from experiments pickle files"""
        print('loading dataset from pickle with %d threads, %d verbosity' % (self.cores, self.verbosity))
        day_dirs = utils.get_day_directories_from_path(self.datadir, self.dates_to_process)

        exp_list = Parallel(n_jobs=self.cores, 
                            verbose=self.verbosity, 
                            backend="threading") \
                           (delayed(self.__deserialize_experiments_from_pickle_worker)
                                   (i, day_dir, pars) for i, day_dir in enumerate(list(day_dirs)))
        exp_list = [item for items in exp_list for item in items]
        self.experiment_list = self.experiment_list + exp_list

    def __deserialize_experiments_from_pickle_worker(self, i, day_dir):
        """worker fn for pickle deserialize"""
        experiment_dirs = [os.path.join(day_dir,dI) for dI in os.listdir(day_dir) 
                           if Path(os.path.join(day_dir,dI)).is_file() and 
                           utils.get_cell_type_from_filename(dI) in self.cell_types]
        exp_list = []
        for j, exp_dir in enumerate(experiment_dirs):
            exp = Experiment(idx=0,path=exp_dir)
            exp_list.append(experiment)
        return exp_list
