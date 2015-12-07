#!/usr/bin/python

import os
import sys
import config
import vtk
import json
import base64
from vtk.util import numpy_support as vtknp

import MainProcess
import External

class Visualization(object):
    """
    Module that handles incomming visualization queries from Portlistener.

    :param inQuery:             Query in JSON format containing at least the keys: 'QuerySubType',
                                    'Parameter'
    :param inDataDirectory:     Directory of incoming volume from a database
    :param camera:              vtkCamera() if the user know what they are doing
    :param outCompressionType:  Compression type of output figures for trasnfering to user, valid types are:
                                    "png", "jpeg"
    :param outDataDirectory:    Directory dicided by the server for storing tmporary file befor transmittion
    :param visualizationJobID:  The job ID of this job, same renderer has same ID
    :return:
    """
    def __init__(self, inQuery, inDataDirectory, camera=None, outCompressionType="png", outDataDirectory="/tmp/ram", visualizationJobID=None):
        super(Visualization, self).__init__()
        self._SetQuery(inQuery)
        self._SetInDataDirectory(str(inDataDirectory))
        self._SetCamera(camera)
        self._SetOutCompressionType(str(outCompressionType))
        self._setOutDataDirectory(str(outDataDirectory))
        self._visualizationJobID = visualizationJobID



    def _GetQuery(self):
        return self._inQuery

    def _GetCamera(self):
        return self._camera

    def _GetJobID(self):
        return self._visualizationJobID

    def _GetOutDataDirectory(self):
        return self._outDataDirectory

    def _GetInDataDirectory(self):
        return self._inDataDirectory

    def _SetOutCompressionType(self, OutCompressionType):
        self._outCompressionType = OutCompressionType

    def _SetQuery(self, Query):
        # TODO: Need to implement type check
        self._inQuery = Query

    def _SetCamera(self, Camera):
        # TODO: Need to implement type check
        self._camera = Camera

    def _SetInDataDirectory(self, indataDirectory):
        if type(indataDirectory) != str:
            raise TypeError("Wrong input type")
            return False
        else:
            self._inDataDirectory = indataDirectory
            return True

    def _setOutDataDirectory(self, outDataDirectory):
        if type(outDataDirectory) != str:
            raise TypeError("Wrong input type")
            return False
        else:
            self._outDataDirectory = outDataDirectory
            return True

    def _reader(self):
        pass

    def ParseQuery(self):
        m_query = self._inQuery
        self._subType = m_query['QuerySubType']
        self._parameter = m_query['Parameter']
        m_parameter = self._parameter
        m_parameter = eval(str(m_parameter))
        # TODO: Query handler for Visualization, Segmentation, Registration and their subtypes
        # If Visualization->SliceView
        # If Visualization->VolumeRendering
        if self._subType == "VolumeRendering":
            # - Initialize variables
            m_contrastRange = m_parameter
            # - Make a renderer
            imageB = self._VolumeRender(m_contrastRange) # renderer assigned to config.rendererDict
            # - Render the image once (Done in _VolumeRender function)

            # - Encode Image File
            imageB = base64.b64encode(imageB)
            # - return renderer to upper layer
            return imageB


        # If Visualization->Rotation
        if self._subType == "Rotation":
            # - Initializae variables
            m_rotationAzimuth, m_rotationElevation = m_parameter
            # - Obtain renderer from upper layer
            renderer = config.rendererDict[str(self._visualizationJobID)]
            renwin = config.renWinDict[str(self._visualizationJobID)]
            # - Obtain camera from renderer
            camera = renderer.GetActiveCamera()
            # - Rotate according to incomming
            camera.Azimuth(m_rotationAzimuth)
            camera.Elevation(m_rotationElevation)
            camera.OrthogonalizeViewUp()
            # camera.Zoom(config.cameraZoomStep[str(self._visualizationJobID)])
            # - Update global dict
            # config.rendererDict[str(self._visualizationJobID)] = renderer
            # - Render Image
            mp = MainProcess.MainProcess()
            # m_path = self._GetOutDataDirectory()+"/current_"+str(self._visualizationJobID)
            # TODO: Allow compatibale compression type, remember to change definition for imageB too

            imageB = mp.ImageWriter(renderer,camera=camera, suppressRender=False,outCompressionType=self._outCompressionType, dimension=config.dimensionDict[self._visualizationJobID])
            # imageB = file(m_path+".%s"%self._outCompressionType,'rb') # - Now write to memory directly
            # - Encode Image File
            imageB = base64.b64encode(imageB)
            return imageB

        # If Visualization-> Zoom:
        if self._subType == "Zoom":
            # - Initialize variables
            m_zoomFactor = m_parameter
            # - Obtain renderer from upper layer
            renderer = config.rendererDict[str(self._visualizationJobID)]
            # - Obtain camera from renderer
            camera = renderer.GetActiveCamera()
            m_distance = camera.GetDistance()
            # - Add restrict zoom at server side, there should be zoom restrictions at client side too

            # - Zoom according to zoom factor
            if not m_zoomFactor:
                config.cameraZoomStep[str(self._visualizationJobID)]*=0.9
                camera.Zoom(0.9)
            else:
                config.cameraZoomStep[str(self._visualizationJobID)]*=1/0.9
                camera.Zoom(1/0.9)

            # - Update global dict
            config.rendererDict[str(self._visualizationJobID)] = renderer
            # Load Main process module
            mp = MainProcess.MainProcess()
            print camera.GetDistance()
            imageB = mp.ImageWriter(renderer, camera=camera, outCompressionType=self._outCompressionType, dimension=config.dimensionDict[self._visualizationJobID])
            # - Encode Image file
            imageB = base64.b64encode(imageB)
            return imageB


        # If Visualization->Translation

        return


    def _VolumeRender(self, m_contrastRange=None):
        # try:
        # TODO: Write document for the parameter of Volume Render
        m_imagePath = str(self._inDataDirectory)         # TODO: Fill in document
        m_acceptedFormat = ['nii', 'vtk', 'DICOM']

        # Handle contrast range
        if m_contrastRange == None:
            m_contrastUpper = None
            m_contrastLower = 0
        else:
            m_contrastUpper = m_contrastRange[1]
            m_contrastLower = m_contrastRange[0]

        # Image type check TODO: nii.gz, DICOM, ECAT, finish nii.gz first
        m_imagePathSplitted = m_imagePath.split('.')
        m_suffix = m_imagePathSplitted[-1]

        # Create rendere first
        renderer = config.rendererDict[str(self._visualizationJobID)]
        renderer.SetBackground(0,0,0)


        # since nifti might be compressed
        if m_suffix == 'gz':
            m_suffix = m_imagePathSplitted[-2]

        if m_acceptedFormat.count(m_suffix) == 0:
            raise TypeError("Wrong input format, currently except %s"%m_acceptedFormat)

        # TODO: Write the following part to a reader function
        # if nifti - Load image as numpy array
        if m_suffix == 'nii':
            m_reader = vtk.vtkNIFTIImageReader()
            m_reader.SetFileName(self._inDataDirectory)

            # -- Use function from Main Process.
            mp = MainProcess.MainProcess()
            m_volume = mp.VolumeRenderingGPURayCast(m_reader, upperThreshold=m_contrastUpper, lowerThreshold=m_contrastLower)
            renderer.AddVolume(m_volume)

        # if vtk - Load by vtk methods
        elif m_suffix == 'vtk':
            m_reader = vtk.vtkPolyDataReader()
            m_reader.SetFileName(m_imagePath)

            # -- Call volume rendering function
            mp = MainProcess.MainProcess()
            m_actor = mp.VolumeRenderingDTILoader(m_reader)
            renderer.AddActor(m_actor)

        # if DICOM - Load VolumeRenderingDICOMLoader, note that if data is dicom, suffix ".DICOM" show be added to the inDataDirectory
        elif m_suffix == 'DICOM':
            # TODO: allows user defined Threshold
            # -- Construct dicom reader for function in main process
            m_reader = vtk.vtkDICOMImageReader()
            m_reader.SetDataByteOrderToLittleEndian() # TODO: allow user input
            m_reader.SetDirectoryName(m_imagePath.replace(".DICOM", ""))
            m_reader.SetDataSpacing(3.2,3.2,1.5) # TODO: allow user input
            m_reader.SetDataOrigin(0,0,0) # TODO: allow user input

            mp = MainProcess.MainProcess()
            m_volume = mp.VolumeRenderingGPUDICOMLoader(m_reader)
            renderer.AddVolume(m_volume)

        renWin = config.renWinDict[str(self._visualizationJobID)]
        renWin.AddRenderer(renderer)
        result = mp.ImageWriter(renderer, renderWin=renWin, dimension=config.dimensionDict[self._visualizationJobID], outCompressionType=self._outCompressionType)
        config.cameraZoomStep[str(self._visualizationJobID)] = 1
        return result

        #
        # except:
        #     print "Error occurs when rendering volume"
        #
        # pass

    def Test(self):
        # vdisplay=xvfbwrapper.Xvfb()
        # vdisplay.start()
        config.dimensionDict['1234'] = [400,400]
        self._SetInDataDirectory('./TestData/pre_t2_brain_50p.nii')
        self._setOutDataDirectory(('./TestData/'))
        ren, im = self.ParseQuery()

        inQuery = {'QuerySubType':"Rotation", 'Parameter':"[10,10]"}
        test._inQuery = inQuery
        # config.rendererDict['1234'] = ren
        test.ParseQuery()
        # vdisplay.stop()

    def TestRotation(self):
        config.dimensionDict['1234'] = [400,400]
        self._SetInDataDirectory('./TestData/pre_t2_brain_50p.nii')
        self._setOutDataDirectory(('./TestData/'))
        self.ParseQuery()


if __name__ == '__main__':
    inQuery = {'QuerySubType':"VolumeRendering", 'Parameter':"None"}
    test = Visualization(inQuery,'./TestData/pre_t2_brain_50p.nii', outCompressionType="jpg" ,visualizationJobID="1234")
    test.Test()

    # inQuery = {'QuerySubType':"Rotation", 'Parameter':"[10,10]"}