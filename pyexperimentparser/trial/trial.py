import numpy as np
import pickle

import engine
try:
    import matlab.engine
except:
    pass

from pathlib import Path

from pyexperimentparser.trial import Bda
from pyexperimentparser.trial import Tpa


class Trial:
    """ Trial

    Parameters
    ----------
    idx : int
        trial index
    bda_fname : string
        path to tpa file
    tpa_fname : string
        path to bda file

    Notes
    -----
    Each trial is associated with one bda file and one tpa file

    Examples
    -----
    """


    def __init__(self, idx, bda_fname, tpa_fname, eng=None):
        #assert  bda, tpa are mat files
        assert Path(bda_fname).is_file(), \
            "bda file does not exist:  %s" % bda_fname
        self.bda_fname = bda_fname
        assert Path(tpa_fname).is_file(), \
            "tpa file does not exist:  %s" % tpa_fname
        self.tpa_fname = tpa_fname

        self.bda_list = []
        self.tpa_list = []
        self.date = ''
        self.idx = idx

        self.load(eng)
        
    def load(self, eng):
        #assert 'eng' in globals(). use global if param eng not none
        _mtlb_tpa = engine.eng.load(self.tpa_fname)
        _mtlb_bda = engine.eng.load(self.bda_fname)

        assert all(key in list(_mtlb_tpa.keys()) for key in ['strROI','strShift']), \
            "tpa malformed %s"  % self.tpa_fname
        assert 'strEvent' in list(_mtlb_bda.keys()),  \
            "bda malformed %s" %  self.bda_fname

        strROIs = _mtlb_tpa['strROI']
        strShifts = _mtlb_tpa['strShift']
        for i, strROI in enumerate(strROIs):
            tmp_tpa = Tpa()
            if i < len(strShifts):
                strShift = strShifts[i]
            else:
                strShift = None
            tmp_tpa.load(strROI, strShift)
            self.tpa_list.append(tmp_tpa)
            
        strEvents = _mtlb_bda['strEvent']
        for strEvent in strEvents:  
            tmp_bda = Bda()
            tmp_bda.load(strEvent)
            self.bda_list.append(tmp_bda)
            
    def plot(self):
        pass
