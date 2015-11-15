'''
Created on Aug 12, 2011
@author: Shareef Dabdoub
'''

import numpy as np
import vtk
import External

class VTKToNumpyMatrix4x4(object):
    def CopyMatrix4x4(self, vtkMatrix):
        """
        Copies the elements of a vtkMatrix4x4 into a numpy array.

        :@type matrix: vtk.vtkMatrix4x4
        :@param matrix: The matrix to be copied into an array.
        :@rtype: numpy.ndarray
        """
        matrix = vtkMatrix
        m = np.ones((4,4))
        for i in range(4):
            for j in range(4):
                m[i,j] = matrix.GetElement(i,j)
        return m


class NumpyToVTKMatrix4x4(object):
    def StoreAsMatrix4x4(self, numpyMatrix):
        """
        Copies the elements of a numpy array into a vtkMatrix4x4.

        :@type: numpy.ndarray
        :@param matrix: The array to be copied into a matrix.
        :@rtype matrix: vtk.vtkMatrix4x4
        """
        m = vtk.vtkMatrix4x4()
        for i in range(4):
            for j in range(4):
                m.SetElement(i, j, numpyMatrix[i,j])
        return m

