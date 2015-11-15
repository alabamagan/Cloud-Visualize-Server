#!/usr/bin/python

import sys

sys.append('./External')
import VTKMatrixConvert

class External(object):
    def __init__(self):
        super(External, self).__init__()
        self.CopyMatrix4x4 = VTKMatrixConvert.CopyMatrix4x4()
        self.StoreAsMatrix4x4 = VTKMatrixConvert.StoreAsMatrix4x4
