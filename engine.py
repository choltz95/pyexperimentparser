import matlab.engine

from pyexperimentparser.dataset.dataset import  Dataset
from pyexperimentparser.experiment.experiment import  Experiment
from pyexperimentparser.trial.trial import Trial
from pyexperimentparser.trial.bda import Bda
from pyexperimentparser.trial.tpa import Tpa

from sys import path
path.append('matlab')

def init():
	global eng
	eng = matlab.engine.start_matlab()