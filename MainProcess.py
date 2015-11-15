#!/usr/bin/python

import sys

sys.path.append('./MainProcess')
import VolumeRendering


class MainProcess(object):
    def __init__(self):
        super(MainProcess, self).__init__()
        self.VolumeRenderingRayCast = VolumeRendering.VolumeRenderingRayCast
        self.ImageWriter = VolumeRendering.ImageWriter

#
#
# if __name__ == '__main__':
#     import nifti
#     worker = MainProcess()
#     pre = nifti.NiftiImage('pre_t2_brain_50p.nii').getDataArray()
#     worker.VolumeRenderingRayCast(pre)