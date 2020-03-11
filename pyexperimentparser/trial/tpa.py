import numpy as np
import pickle

from joblib import Parallel, delayed

import matlab.engine
import engine

import random

class Tpa:
    """ TPA

    Parameters
    ----------

    Notes
    -----

    Examples
    -----
    """


    def __init__(self):
        self.idx = 0
        self.fname = ''
        self.shifts = []
        self.roi = []

        # Selected ROI properties
        # init common ROI structure
        self.Type                = 0               # define ROI type
        self.State               = 0               # designates in which init state ROI is in
        self.Color               = random.randint(1,4)       # generate colors
        self.Name                = 'X'             # which name
        self.SeqNum              = 0               # event numbering
        self.AverType            = 0               # which operation to perform
        self.CellPart            = 1
        self.CountId             = 1               # T`BD

        self.xyInd               = []               # shape in xy plane
        self.ytInd               = []               # shape in yt plane

        # bounding box
        self.xInd                = [1, 1]           # range location in X
        self.yInd                = [1, 1]           # range location in Y
        self.zInd                = [1, 1]           # range location in Z stack
        self.tInd                = [1, 1]           # rangelocation in T stack

        # Data 
        self.LineInd             = []               # pixels indices of ROI center or ROI line
        self.PixInd              = []               # pixels indeces of ROI mask in image plane used for ROI mean dF/F computation
        self.Data                = []              # processed data for ROI - mean, dF/F, Spike
        self.procROI             = []              # processed dF/F
        #        Spike               = []              # spikes extracted

        # init graphics
        self.ViewType            = 1               # which type default
        self.NameShow            = False           # manage show name
        self.ViewXY              = []             # structure contains XY shape params
        self.ViewYT              = []             # structure contains YT shape params

        # clicks position
        self.pointRef                    = [10, 10]  # point1        
        self.rectangleInitialPosition    = [-1, -1, -1, -1] #rectangle to move
        self.shapeInitialDrawing         = [0, 0] # coordinates of the shape

        # internal stuff
        #cntxMenu            = []  # handle that will contain context menu

        # TESTING
        self.hFigure             = []
        self.hAxes               = []
        self.hImage              = []


        # PRIVATE
        #         # global constants see Par file
        self.STATE_TYPES         = {'NONE':1,'INIT':2,'VIEWXY':3,'VIEWYT':4,'VIEWALL':5}
        self.VIEW_TYPES          = {'XY':1,'YT':2,'XYYT':3}
        self.ROI_TYPES           = {'RECT':1,'ELLIPSE':2,'FREEHAND':3}
        self.ROI_AVERAGE_TYPES   = {'MEAN':1,'LOCAL_MAXIMA':2,'LINE_ORTHOG':3}
        

    def load(self, strRoi, strShift):
        properties = engine.eng.properties(strRoi)
        engine.eng.workspace["temp_obj"] = strRoi
        for prop in properties:
            prop_query = engine.eng.eval("temp_obj."+prop)
            if prop == 'procROI':
                continue
            elif prop == 'Data':
                setattr(self, prop, np.asarray(prop_query))
                self.procROI = self.Data[:,1]
            else:
                setattr(self, prop, prop_query)

        self.shifts.append(strShift)

    def print_param(self):
        print("TPA: ","idx: ", self.idx, " fname: ", self.fname, " type: ", self.Type, 
            " state: ", self.State, " name: ", self.Name, " seqnum: ", self.SeqNum,
            " avertype: ", self.AverType, " CellPart: ", self.CellPart, " countid: ", self.CountId)
                
