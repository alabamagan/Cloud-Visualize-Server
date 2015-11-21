#!/usr/bin/python

import os

"""
All the global variable excep for pid is of the diction format which
key-value pairs are according to the name of the dictionary:
    {ValueType}Dict = {'{jobIDs}': {Value}}
"""
dimensionDict = {}
rendererDict = {}
renWinDict = {}
cameraDict = {}
cameraZoomStep = {}
pid = os.getpid()
vdisplay = False