#!/usr/bin/python

import os

"""
All the global variable excep for pid is of the diction format which
key-value pairs are according to the name of the dictionary:
    {ValueType}Dict = {'{jobIDs}': {Value}}
"""
dimensionDict = {}
rendererDict = {}
cameraDict = {}
pid = os.getpid()