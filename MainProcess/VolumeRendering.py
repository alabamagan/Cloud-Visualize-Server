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

def VolumeRenderingGPUDICOMLoader(dicomreader):


    imcast = vtk.vtkImageCast()
    imcast.SetInputConnection(dicomreader.GetOutputPort())
    imcast.SetOutputScalarTypeToUnsignedShort()
    imcast.ClampOverflowOn()

    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(-2048, 0, 0.5, 0)
    opacityTransferFunction.AddPoint(142.677, 0, 0.5, 0)
    opacityTransferFunction.AddPoint(145.016, 0.116071, 0.5, 0.26)
    opacityTransferFunction.AddPoint(192.174, 0.5625, 0.469638, 0.39)
    opacityTransferFunction.AddPoint(217.24, 0.776786, 0.666667, 0.41)
    opacityTransferFunction.AddPoint(384.347, 0.830357, 0.5, 0)
    opacityTransferFunction.AddPoint(3661, 0.830357, 0.5, 0)

    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(-2048, 0, 0, 0, 0.5, 0)
    colorTransferFunction.AddRGBPoint(142.667, 0, 0, 0, 0.5, 0)
    colorTransferFunction.AddRGBPoint(145.016, 0.615686, 0, 0.156863, 0.5, 0.26)
    colorTransferFunction.AddRGBPoint(192.174, 0.909804, 0.454902, 0, 0.469638, 0.39)
    colorTransferFunction.AddRGBPoint(217.24, 0.972549, 0.807843, 0.611765, 0.666667, 0.41)
    colorTransferFunction.AddRGBPoint(384.347, 0.909804, 0.909804, 1, 0.5, 0)
    colorTransferFunction.AddRGBPoint(3661, 1, 1, 1, 0.5, 0)
    colorTransferFunction.ClampingOn()
    colorTransferFunction.SetColorSpace(1)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetAmbient(0.2)
    volumeProperty.SetDiffuse(1)
    volumeProperty.SetSpecular(0)
    volumeProperty.SetSpecularPower(1)
    volumeProperty.DisableGradientOpacityOn()
    volumeProperty.SetComponentWeight(1, 1)
    volumeProperty.GetScalarOpacityUnitDistance(0.48117)
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.SetInterpolationTypeToLinear()

    raycast = vtk.vtkVolumeRayCastCompositeFunction()
    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(imcast.GetOutputPort())
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetSampleDistance(0.1)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # === DEBUG TEST ===
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    vdisplay = xvfbwrapper.Xvfb()
    vdisplay.start()

    print "writing"
    ImageWriter(renderer, outFileName="tmp1")
    print "write 1..."
    camera = renderer.GetActiveCamera()
    camera.Zoom(1.3)
    camera.Azimuth(40)
    ImageWriter(renderer, camera=camera, outFileName="tmp2")
    print "write 2..."
    renderer.ResetCameraClippingRange()
    vdisplay.stop()
    # === DEBUG TEST ===
    return volume

def VolumeRenderingDICOMLoader(dicomreader):


    imcast = vtk.vtkImageCast()
    imcast.SetInputConnection(dicomreader.GetOutputPort())
    imcast.SetOutputScalarTypeToUnsignedShort()
    imcast.ClampOverflowOn()

    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(-2048, 0, 0.5, 0)
    opacityTransferFunction.AddPoint(142.677, 0, 0.5, 0)
    opacityTransferFunction.AddPoint(145.016, 0.116071, 0.5, 0.26)
    opacityTransferFunction.AddPoint(192.174, 0.5625, 0.469638, 0.39)
    opacityTransferFunction.AddPoint(217.24, 0.776786, 0.666667, 0.41)
    opacityTransferFunction.AddPoint(384.347, 0.830357, 0.5, 0)
    opacityTransferFunction.AddPoint(3661, 0.830357, 0.5, 0)

    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(-2048, 0, 0, 0, 0.5, 0)
    colorTransferFunction.AddRGBPoint(142.667, 0, 0, 0, 0.5, 0)
    colorTransferFunction.AddRGBPoint(145.016, 0.615686, 0, 0.156863, 0.5, 0.26)
    colorTransferFunction.AddRGBPoint(192.174, 0.909804, 0.454902, 0, 0.469638, 0.39)
    colorTransferFunction.AddRGBPoint(217.24, 0.972549, 0.807843, 0.611765, 0.666667, 0.41)
    colorTransferFunction.AddRGBPoint(384.347, 0.909804, 0.909804, 1, 0.5, 0)
    colorTransferFunction.AddRGBPoint(3661, 1, 1, 1, 0.5, 0)
    colorTransferFunction.ClampingOn()
    colorTransferFunction.SetColorSpace(1)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetAmbient(0.2)
    volumeProperty.SetDiffuse(1)
    volumeProperty.SetSpecular(0)
    volumeProperty.SetSpecularPower(1)
    volumeProperty.DisableGradientOpacityOn()
    volumeProperty.SetComponentWeight(1, 1)
    volumeProperty.GetScalarOpacityUnitDistance(0.48117)
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.SetInterpolationTypeToLinear()

    raycast = vtk.vtkVolumeRayCastCompositeFunction()
    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetVolumeRayCastFunction(raycast)
    volumeMapper.SetInputConnection(imcast.GetOutputPort())
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetSampleDistance(0.1)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # === DEBUG TEST ===
    # renderer = vtk.vtkRenderer()
    # renderer.AddVolume(volume)
    # vdisplay = xvfbwrapper.Xvfb()
    # vdisplay.start()
    #
    # print "writing"
    # ImageWriter(renderer, outFileName="tmp1")
    # print "write 1..."
    # camera = renderer.GetActiveCamera()
    # camera.Zoom(1.3)
    # camera.Azimuth(40)
    # ImageWriter(renderer, camera=camera, outFileName="tmp2")
    # print "write 2..."
    # renderer.ResetCameraClippingRange()
    # vdisplay.stop()
    # === DEBUG TEST ===
    return volume

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

def TestGPUVolumeRender():
    reader = vtk.vtkDICOMImageReader()
    reader.SetDataByteOrderToLittleEndian()
    reader.SetDirectoryName("../TestData/cta_output")
    reader.SetDataSpacing(3.2,3.2,1.5)
    reader.SetDataOrigin(0,0,0)
    vol = VolumeRenderingGPUDICOMLoader(reader)

if __name__ == '__main__':
    TestGPUVolumeRender()