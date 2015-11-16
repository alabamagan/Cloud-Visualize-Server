#!/usr/bin/python

import vtk
import numpy as np
import nifti
import xvfbwrapper

def VolumeRenderingDTILoader(inVTKPolyDataReader):
    reader = inVTKPolyDataReader
    reader.GetOutput().GetCellData().SetActiveScalars("Average Direction")
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

def VolumeRenderingRayCast(inVolume, scale=[1,1,1], lowerThereshold=0, upperThereshold=None):
    inVolume = np.ushort(inVolume)
    inVolumeShape = inVolume.shape
    inVolumeString = inVolume.tostring()

    # Color map related
    if upperThereshold == None:
        upperThereshold = inVolume.max()

    if upperThereshold <= lowerThereshold:
        raise ValueError("Upper thereshold must be larger than lower thereshold.")

    centerThereshold = (upperThereshold - lowerThereshold)/2. + lowerThereshold
    lowerQuardThereshold = (centerThereshold - lowerThereshold)/2. + lowerThereshold
    upperQuardThereshold = (upperThereshold - centerThereshold)/2. + centerThereshold

    dataImporter = vtk.vtkImageImport()
    dataImporter.CopyImportVoidPointer(inVolumeString, len(inVolumeString))
    dataImporter.SetDataScalarTypeToUnsignedShort()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, inVolume.shape[2]-1, 0, inVolume.shape[1]-1, 0, inVolume.shape[0]-1)
    dataImporter.SetWholeExtent(0, inVolume.shape[2]-1, 0, inVolume.shape[1]-1, 0, inVolume.shape[0]-1)

    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(lowerThereshold, 0)
    alphaChannelFunc.AddPoint(lowerQuardThereshold, 0.05)
    alphaChannelFunc.AddPoint(centerThereshold, 0.4)
    alphaChannelFunc.AddPoint(upperQuardThereshold, 0.05)
    alphaChannelFunc.AddPoint(upperThereshold, 0)

    colorFunc = vtk.vtkColorTransferFunction()
    colorFunc.AddRGBPoint(lowerThereshold, 0, 0, 0)
    colorFunc.AddRGBPoint(centerThereshold, 0.5, .5, .5)
    colorFunc.AddRGBPoint(upperThereshold, .8, .8, .8)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)

    compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetVolumeRayCastFunction(compositeFunction)
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    volume.SetScale(scale)

    # Volume is returned for further rendering
    return volume

def ImageWriter(renderer, camera=None, outCompressionType="jpg", outFileName="tmp", suppress=False, dimension=[400,400]):
    """
    Write image from renderer to a figure.


    :param renderer:            vtkRenderer
    :param dimension            (Optional)Dimension of output, e.g. [x, y]
    :param camera:              (Optional)vtkCameraObject
    :param outCompressionType:  (Optional)Specify output format, support "png", "jpeg", default to "png"
    :param outFileName:         (Optional)Filename of the output
    :param supress:             (Optional)Suppress output file
    :return:

    Note:
        Depending on the version of vtk and graphics driver,
    the vtkRenderWindow.SetOffScreenRendering(1) may behave strangely, it is therefore adviced
    to use the xvfbwrapper if you are hosting a headless server and comment the line that writes
    renderWin.SetOffScreenRendering(1) in this function.
    """
    renderWin = vtk.vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderWin.SetSize(dimension[0], dimension[1])
    renderWin.SetOffScreenRendering(1)

    # ** Note that rendering does not work with the interactor. **

    renderWin.Render()

    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWin)
    windowToImageFilter.Update()

    if camera != None:
        renderer.SetActiveCamera(camera)

    # Writer the render to image
    if outCompressionType == 'png':
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(outFileName+".png")

    if outCompressionType == 'jpeg' or outCompressionType == 'jpg':
        writer = vtk.vtkJPEGWriter()
        writer.SetFileName(outFileName+".jpg")

    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    if suppress==False:
        writer.Write()
    pass


def TestRayCase():
    pre = nifti.NiftiImage('../TestData/pre_t2_brain_50p.nii')
    preD = pre.getDataArray()
    scale = pre.header['pixdim'][1:4]

    vdisplay = xvfbwrapper.Xvfb(width=1024, height=768, colordepth=24)
    vdisplay.start()

    volume = VolumeRenderingRayCast(preD, scale)
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    ImageWriter(renderer, outFileName="Initialize") # Must render once before you get camera
    camera = renderer.GetActiveCamera()

    vdisplay.stop()
    pass

def TestDTILoader():
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName("../TestData/tract.vtk")
    actor = VolumeRenderingDTILoader(reader)

    vdisplay = xvfbwrapper.Xvfb(width=1024, height=768, colordepth=24)
    vdisplay.start()

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0,0,0)
    ImageWriter(renderer, outFileName="tractTest", dimension=[800,800])

    vdisplay.stop()

if __name__ == '__main__':
    TestDTILoader()