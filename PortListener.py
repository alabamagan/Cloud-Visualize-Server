#!/usr/bin/python

import os
import config
import pyjsonrpc
import base64
import signal
from Visualization import *

def Prober():
    return os.getpid()

# TODO: Add compression type to the parameters
def Visualize(subType, parameter, subjectID, projectID, imageID, dimension, userID):
    message =  "Visualization is requested with following parameters \n " \
               "subType: \t%s\n" \
               "parameter: \t%s\n" \
               "subjectID: \t%s\n" \
               "projectID: \t%s\n" \
               "dimension: \t %s\n" \
               "imageID: \t%s\n"%(subType, parameter, subjectID, projectID, dimension, imageID)

    # Initialize Varaibles & Type check
    print message
    dimension = list(eval(str(dimension)))
    visualizationJobID="%sv"%userID
    if len(dimension) != 2:
        raise IndexError("Dimension input is the dimension of the output picture and it must be of len==2")

    config.dimensionDict[visualizationJobID] = list(dimension)
    # Rebuild inQuery
    Query = {}
    Query['QuerySubType'] = subType
    Query['Parameter'] = parameter
    # call visualization.ParseQuery(), require it to return renderer and initial rendered picture file
    g = Visualization(Query, outCompressionType="jpg",inDataDirectory=os.path.abspath('.')+"/TestData/%s"%subjectID, outDataDirectory="/tmp/ram/cldv/%s"%config.pid, visualizationJobID=visualizationJobID)

    # If Visualization->volume renderering
    if subType == "VolumeRendering":
        renderer = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        config.cameraZoomStep[visualizationJobID] = 1 # Set ZoomStep
        config.rendererDict[visualizationJobID] = renderer # This keeps the renderer alive for the rest of the operation
        config.renWinDict[visualizationJobID] = renWin
        imagefile = g.ParseQuery()

    if subType == "Rotation":
        imagefile = g.ParseQuery()
    if subType == "Zoom":
        imagefile = g.ParseQuery()
    return imagefile

def Registration():
    pass

def Segmentation():
    pass


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    methods = dict(
        Visualize=Visualize,
        Prober=Prober
    )


if __name__ == '__main__':
    locker = "/tmp/clv.pid"
    if os.path.isfile(locker):
        raise SystemError("Lock file /tmp/clv.pid exist")
    else:
        # Threading HTTP-Server
        serverIP = '137.189.141.216'
        http_server = pyjsonrpc.ThreadingHttpServer(
            server_address = (serverIP, 43876),
            RequestHandlerClass = RequestHandler
        )
        print "Starting HTTP server ..."
        print "URL: http://%s:43876"%serverIP
        try:
            # lockerfile = file(locker, 'w')
            # lockerfile.write("%s"%os.getpid())
            # lockerfile.close()
            # if not os.path.isdir("/tmp/ram/cldv/%s"%config.pid):
            #     os.system("mkdir -p /tmp/ram/cldv/%s"%config.pid)
            # if config.vdisplay:
            #     vdisplay = xvfbwrapper.Xvfb()
            #     vdisplay.start()
            http_server.serve_forever()
        except KeyboardInterrupt:
            http_server.shutdown()
            # os.remove(locker)
            # os.system("rm -rf /tmp/ram/cldv")
            # if config.vdisplay:
            #     vdisplay.stop()




