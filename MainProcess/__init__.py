import VolumeRendering

class MainProcess(object):
    def __init__(self):
        super(MainProcess, self).__init__()
        self.VolumeRenderingRayCast = VolumeRendering.VolumeRenderingRayCast
        self.VolumeRenderingDTILoader = VolumeRendering.VolumeRenderingDTILoader
        self.VolumeRenderingDICOMLoader = VolumeRendering.VolumeRenderingDICOMLoader
        self.ImageWriter = VolumeRendering.ImageWriter

