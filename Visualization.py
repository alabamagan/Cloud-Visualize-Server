#!/usr/bin/python

import os
import sys
import config
import vtk
import json
import nifti
import base64
import xvfbwrapper
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
            renderer = self._VolumeRender(m_contrastRange)
            # - Render the image once (Done in _VolumeRender function)
            m_path = self._GetOutDataDirectory()+"/%s_Initialize.%s"%(self._visualizationJobID, self._outCompressionType)
            imageB = file(m_path,'rb')
            # - Encode Image File
            imageB = base64.b64encode(imageB.read())
            # - return renderer to upper layer
            return renderer, imageB


        # If Visualization->Rotation
        if self._subType == "Rotation":
            # - Initializae variables
            m_rotationAzimuth, m_rotationElevation = m_parameter
            # - Obtain renderer from upper layer
            renderer = config.rendererDict[str(self._visualizationJobID)]
            # - Obtain camera from renderer
            camera = renderer.GetActiveCamera()
            # - Rotate according to incomming
            camera.Azimuth(m_rotationAzimuth)
            camera.Elevation(m_rotationElevation)
            camera.OrthogonalizeViewUp()
            # - Update global dict
            config.rendererDict[str(self._visualizationJobID)] = renderer
            # - Render Image
            mp = MainProcess.MainProcess()
            m_path = self._GetOutDataDirectory()+"/current_"+str(self._visualizationJobID)
            # TODO: Allow compatibale compression type, remember to change definition for imageB too
            mp.ImageWriter(renderer, camera=camera, outCompressionType=self._outCompressionType, outFileName=(m_path), dimension=config.dimensionDict[self._visualizationJobID])
            imageB = file(m_path+".%s"%self._outCompressionType,'rb')
            # - Encode Image File
            imageB = base64.b64encode(imageB.read())
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
            if config.cameraZoomStep.has_key(str(self._visualizationJobID)):
                m_zoomStep = config.cameraZoomStep[str(self._visualizationJobID)]
            else:
                m_zoomStep = m_distance/5.
            # - Zoom according to zoom factor
            if m_zoomFactor and m_distance - m_zoomStep > m_zoomStep:
                camera.SetDistance(m_distance - m_zoomStep)
            elif not m_zoomFactor and m_distance + m_zoomStep < 10*m_zoomStep:
                camera.SetDistance(m_distance + m_zoomStep)
            mp.ImageWriter(renderer, camera=camera, outCompressionType=self._outCompressionType, outFileName=(m_path), dimension=config.dimensionDict[self._visualizationJobID])
            # - Encode Image file
            imageB = file(m_path+".%s"%self._outCompressionType, 'rb')
            imageB = base64.b64encode(imageB.read())
            return imageB


        # If Visualization->Translation




        return


    def _VolumeRender(self, m_contrastRange=None):
        try:
            # TODO: Write document for the parameter of Volume Render
            m_imagePath = str(self._inDataDirectory)         # TODO: Fill in document
            m_acceptedFormat = ['nii', 'vtk']

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

            renderer = vtk.vtkRenderer()
            renderer.SetBackground(0,0,0)

            # since nifti might be compressed
            if m_suffix == 'gz':
                m_suffix = m_imagePathSplitted[-2]

            if m_acceptedFormat.count(m_suffix) == 0:
                raise TypeError("Wrong input format, currently except %s"%m_acceptedFormat)

            # TODO: Write the following part to a reader function
            # if nifti - Load image as numpy array
            if m_suffix == 'nii':
                m_volume = nifti.NiftiImage(m_imagePath)
                m_volumeData = m_volume.getDataArray()
                m_volumeHeader = m_volume.header
                m_volumeScale = m_volumeHeader['pixdim'][1:4]

                # -- Use function from Main Process.
                mp = MainProcess.MainProcess()

                m_volume = mp.VolumeRenderingRayCast(m_volumeData, scale=m_volumeScale, upperThereshold=m_contrastUpper, lowerThereshold=m_contrastLower)
                renderer.AddVolume(m_volume)

            # if vtk - Load by vtk methods
            elif m_suffix == 'vtk':
                m_reader = vtk.vtkPolyDataReader()
                m_reader.SetFileName(m_imagePath)

                # -- Call volume rendering function
                mp = MainProcess.MainProcess()
                m_actor = mp.VolumeRenderingDTILoader(m_reader)
                renderer.AddActor(m_actor)

            mp.ImageWriter(renderer, outFileName=self._GetOutDataDirectory()+"/%s_Initialize"%self._visualizationJobID, dimension=config.dimensionDict[self._visualizationJobID], outCompressionType=self._outCompressionType)
            return renderer


        except:
            print "Error occurs when rendering volume"

        pass

    def Test(self):
        self._SetInDataDirectory('./TestData/pre_t2_brain_50p.nii')
        self._VolumeRender()


if __name__ == '__main__':
    test = Visualization('inQuery','./TestData/pre_t2_brain_50p.nii','what', 'camera', 'outcompressionType', 'jobid' )
    test.Test()