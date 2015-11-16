#!/usr/bin/python

import VTKMatrixConvert

class External(object):
    def __init__(self):
        super(External, self).__init__()
        self._objNumpyToVTK = VTKMatrixConvert.NumpyToVTKMatrix4x4()
        self._objVTKToNumpy = VTKMatrixConvert.VTKToNumpyMatrix4x4()
        self.NumpyToVTK = self._objNumpyToVTK.StoreAsMatrix4x4
        self.VTKToNumpy = self._objVTKToNumpy.CopyMatrix4x4