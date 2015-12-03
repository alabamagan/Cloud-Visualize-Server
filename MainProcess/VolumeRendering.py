#!/usr/bin/python

import sys
import vtk

sys.path.append("../")
import config
import numpy as np


def VolumeRenderingDTILoader(inVTKPolyDataReader):
    """
    Recieve a vtkPolyDataReader and return correspond actor. Reader can be created in the
    following manner:
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName("path.vtk")

    :param inVTKPolyDataReader:
    :return:
    """
    reader = inVTKPolyDataReader
    reader.GetOutput().GetCellData().SetActiveScalars("Average Direction")
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


def VolumeRenderingGPUDICOMLoader(dicomreader):
    """
    Recieve a vtkDICOMImageReader and return the volume actor. Reader can be created in
    the following manner:

        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(path)
        reader.SetDataSpacing(3.2,3.2,1.5)  # Set slice spacing
        reader.SetDataOrigin(0,0,0)

    :param dicomreader: vtkDICOMImageReader()
    :return: vtkVolume()
    """
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
    volumeProperty.SetScalarOpacityUnitDistance(0.48117)
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.SetInterpolationTypeToLinear()

    # raycast = vtk.vtkVolumeRayCastCompositeFunction()
    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(imcast.GetOutputPort())
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetSampleDistance(0.1)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # === DEBUG TEST ===
    # renderer = vtk.vtkRenderer()
    # renderer.AddVolume(volume)
    #
    #
    # print "writing"
    # ImageWriter(renderer, outFileName="tmp1")
    # print "write finish"
    # camera = renderer.GetActiveCamera()
    # camera.Zoom(1.3)
    # camera.Azimuth(40)
    # ImageWriter(renderer, camera=camera, outFileName="tmp2", AAFrames=0)
    # print "write cam1"
    # camera.Zoom(1.3)
    # camera.Azimuth(40)
    # ImageWriter(renderer, camera=camera, outFileName="tmp3", AAFrames=0)
    # print "write cam2"
    # camera.Zoom(1.3)
    # camera.Azimuth(40)
    # ImageWriter(renderer, camera=camera, outFileName="tmp4", AAFrames=0)
    # print "write cam3"
    # renderer.ResetCameraClippingRange()

    # === DEBUG TEST ===
    return volume


def VolumeRenderingDICOMLoader(dicomreader):
    """
    (Not used)

    :param dicomreader:
    :return:
    """

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
    volumeProperty.SetScalarOpacityUnitDistance(0.48117)
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.SetInterpolationTypeToLinear()

    raycast = vtk.vtkVolumeRayCastCompositeFunction()
    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetVolumeRayCastFunction(raycast)
    volumeMapper.SetInputConnection(imcast.GetOutputPort())
    # volumeMapper.SetBlendModeToComposite()
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

def VolumeRenderingGPURayCast(volumereader, scale=None, lowerThreshold=0, upperThreshold=None):
    """
    Ray cast function using GPU general for most volume readers.
    :param volumereader:        vtk file reader for 3D images
    :param scale:               scale [x, y, z] of the slice/voxel spacing to real.
                                    Default = [ volumereader.GetNIFTIHeader().GetPixDim(i) for i in xrange(3)]
    :param lowerThreshold:      lower Threshold for raycast. Default = 0
    :param upperThreshold:      upper Threshold for raycast. Default = volumereader.GetOutput().GetScalarRange()[1]
    :return:

    Note: This function requires your version of VTK being compiled with the use of
    GPU-proprietary libGL.so. The cmake option is OPEN_gl_LIBRARY for VTK 6.3.0. This
    is more trickier in Linux and is potentially more unstable. For your reference
    this program is entirely build against nVidia-352 Linux driver.
    """

    reader = volumereader
    reader.Update()
    header = reader.GetNIFTIHeader()

    # Insert Default value if none provided
    if scale == None:
        scale = [abs(header.GetPixDim(i)) for i in xrange(3) ]    # Insert Default value if none provided
    if scale == None:
        scale = [abs(header.GetPixDim(i)) for i in xrange(3) ]
    if upperThreshold == None:
        upperThreshold = reader.GetOutput().GetScalarRange()[1]

    # Error check
    if lowerThreshold >= upperThreshold:
        raise ValueError("UpperThreshold cannot be smaller than lowerThreshold")





    # Set some default color points
    centerThreshold = (upperThreshold - lowerThreshold) / 2. + lowerThreshold
    lowerQuardThreshold = (centerThreshold - lowerThreshold) / 2. + lowerThreshold
    upperQuardThreshold = (upperThreshold - centerThreshold) / 2. + centerThreshold

    # Set some default alpha map
    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(lowerThreshold, 0)
    alphaChannelFunc.AddPoint(lowerQuardThreshold, 0.05)
    alphaChannelFunc.AddPoint(centerThreshold, 0.4)
    alphaChannelFunc.AddPoint(upperQuardThreshold, 0.05)
    alphaChannelFunc.AddPoint(upperThreshold, 0)

    colorFunc = vtk.vtkColorTransferFunction()
    colorFunc.AddRGBPoint(lowerThreshold, 0, 0, 0)
    colorFunc.AddRGBPoint(centerThreshold, 0.5, .5, .5)
    colorFunc.AddRGBPoint(upperThreshold, .8, .8, .8)


    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)

    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    volume.SetScale(scale)

    return volume

def VolumeRenderingRayCast(inVolume, scale=[1, 1, 1], lowerThreshold=0, upperThreshold=None):
    """
    Recieve a numpy volume and render it with RayCast method. This method employs CPU raycast
    and will subject to upgrades of using GPUVolumeMapper in the future. The method returns
    a vtkVolume actor which can be added to a vtkRenderer

    :param inVolume:        numpy volume
    :param scale:           scale [x, y, z] of the slice/voxel spacing to real spacing
    :param lowerThreshold:  lower Threshold for raycast. Default = 0
    :param upperThreshold:  upper Threshold for raycast. Default = inVolume.max()
    :return: vtk.vtkVolume
    """
    inVolume = np.ushort(inVolume)
    inVolumeString = inVolume.tostring()

    # Color map related
    if upperThreshold == None:
        upperThreshold = inVolume.max()

    if upperThreshold <= lowerThreshold:
        raise ValueError("Upper Threshold must be larger than lower Threshold.")

    centerThreshold = (upperThreshold - lowerThreshold) / 2. + lowerThreshold
    lowerQuardThreshold = (centerThreshold - lowerThreshold) / 2. + lowerThreshold
    upperQuardThreshold = (upperThreshold - centerThreshold) / 2. + centerThreshold

    dataImporter = vtk.vtkImageImport()
    dataImporter.CopyImportVoidPointer(inVolumeString, len(inVolumeString))
    dataImporter.SetDataScalarTypeToUnsignedShort()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, inVolume.shape[2] - 1, 0, inVolume.shape[1] - 1, 0, inVolume.shape[0] - 1)
    dataImporter.SetWholeExtent(0, inVolume.shape[2] - 1, 0, inVolume.shape[1] - 1, 0, inVolume.shape[0] - 1)

    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(lowerThreshold, 0)
    alphaChannelFunc.AddPoint(lowerQuardThreshold, 0.05)
    alphaChannelFunc.AddPoint(centerThreshold, 0.4)
    alphaChannelFunc.AddPoint(upperQuardThreshold, 0.05)
    alphaChannelFunc.AddPoint(upperThreshold, 0)

    colorFunc = vtk.vtkColorTransferFunction()
    colorFunc.AddRGBPoint(lowerThreshold, 0, 0, 0)
    colorFunc.AddRGBPoint(centerThreshold, 0.5, .5, .5)
    colorFunc.AddRGBPoint(upperThreshold, .8, .8, .8)

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


def ImageWriter(renderer, camera=None, outCompressionType="jpg", suppress=False,
                dimension=[400, 400], AAFrames=5):
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
    the vtkRenderWindow.SetOffScreenRendering(1) may behave strangely, it is therefore advised
    to use the xvfbwrapper if you are hosting a headless server and comment the line that writes
    renderWin.SetOffScreenRendering(1) in this function.
        Alternatively, if you managed to compile VTK from souce with the option VTK_USE_OFFSCREEN
    on then you might simply use SetOffScreenRendering(1)/OffScreenRenderingOn() and suppress
    xvfbwrapper through the code by setting config.vdisplay=False
    """

    renderWin = vtk.vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderWin.OffScreenRenderingOn()
    renderWin.SetSize(int(dimension[0]), int(dimension[1]))

    renderWin.Render() # TODO: Error for nifti here
    renderWin.SetAAFrames(AAFrames)
    # ** Note that rendering does not work with the interactor. **

    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWin)
    windowToImageFilter.Update()

    if camera != None:
        renderer.SetActiveCamera(camera)

    # Writer the render to image
    if outCompressionType == 'png':
        writer = vtk.vtkPNGWriter()

    if outCompressionType == 'jpeg' or outCompressionType == 'jpg':
        writer = vtk.vtkJPEGWriter()


    writer.SetWriteToMemory(1)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    if suppress == False:
        writer.Write()
        result = writer.GetResult()
    return result


# def TestRayCast():
#     """
#     Test Ray Cast Usage, uncomment the DEBUG TEST lines before use
#     :return:
#     """
#     pre = nifti.NiftiImage('../TestData/pre_t2_brain_50p.nii')
#     preD = pre.getDataArray()
#     scale = pre.header['pixdim'][1:4]
#
#     vdisplay = xvfbwrapper.Xvfb(width=1024, height=768, colordepth=24)
#     vdisplay.start()
#
#     volume = VolumeRenderingRayCast(preD, scale)
#     renderer = vtk.vtkRenderer()
#     renderer.AddVolume(volume)
#     ImageWriter(renderer, outFileName="Initialize")  # Must render once before you get camera
#     camera = renderer.GetActiveCamera()
#
#     vdisplay.stop()
#     pass
#

# def TestDTILoader():
#     """
#     Testing DTI Usage with tract5000.vtk
#     :return:
#     """
#     reader = vtk.vtkPolyDataReader()
#     reader.SetFileName("../TestData/tract5000.vtk")
#     actor = VolumeRenderingDTILoader(reader)
#
#     if config.vdisplay:
#         vdisplay = xvfbwrapper.Xvfb(width=1024, height=768, colordepth=24)
#         vdisplay.start()
#
#     renderer = vtk.vtkRenderer()
#     renderer.AddActor(actor)
#     renderer.SetBackground(0, 0, 0)
#     renWin = vtk.vtkRenderWindow()
#     renWin.AddRenderer(renderer)
#     ImageWriter(renderer, outFileName="tractTest", dimension=[800, 800])
#     camera = renderer.GetActiveCamera()
#     # camera.Zoom(1.5)
#     # camera.Azimuth(30)
#     # camera.Elevation(30)
#     # ImageWriter(renderer, outFileName="tractTest", dimension=[800, 800])
#     if config.vdisplay:
#         vdisplay.stop()
#

def TestVolumeRender():
    """
    Test DICOM loader usage, uncomment the DEBUG TEST lines before use
    :return:
    """
    reader = vtk.vtkDICOMImageReader()
    reader.SetDataByteOrderToLittleEndian()
    reader.SetDirectoryName("../TestData/cta_output")
    reader.SetDataSpacing(3.2, 3.2, 1.5)
    reader.SetDataOrigin(0, 0, 0)
    vol = VolumeRenderingDICOMLoader(reader)
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(vol)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)

    # vdisplay = xvfbwrapper.Xvfb()
    # vdisplay.start()
    ImageWriter(renderer, outFileName="tmp")
    renderer.GetActiveCamera().Azimuth(40)
    ImageWriter(renderer, outFileName="tmp2")
    # vdisplay.stop()


def TestGPUVolumeRender():
    """
    Test GPU DICOM Loader Usage, uncomment the DEBUG TEST lines before use
    :return:
    """
    reader = vtk.vtkDICOMImageReader()
    reader.SetDataByteOrderToLittleEndian()
    reader.SetDirectoryName("../TestData/cta_output")
    reader.SetDataSpacing(3.2, 3.2, 1.5)
    reader.SetDataOrigin(0, 0, 0)
    print "test"
    vol = VolumeRenderingGPUDICOMLoader(reader)
    # renderer = vtk.vtkRenderer()
    # renderer.AddVolume(vol)
    # ImageWriter(renderer, outFileName="gg")
    # renderer.GetActiveCamera().Azimuth(40)
    # ImageWriter(renderer, outFileName="gg2")

if __name__ == '__main__':
    TestGPUVolumeRender()
