#!/usr/bin/python

#git tag: v1.1-pypi
""" A threaded server based on a JsonServer object in the jsonSocket module """
import threading
import socket
import logging

import PortListener

logger = logging.getLogger("threadedServer")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT, filename="thdsev.log")

class ThreadedServer(threading.Thread, PortListener.JsonServer):
    def __init__(self, **kwargs):
        super(ThreadedServer, self).__init__()
        threading.Thread.__init__(self)
        PortListener.JsonServer.__init__(self)
        self._isAlive = False

    def _processMessage(self, obj):
        """

        :param obj:
        :return:
        """
        print obj
        pass

    def run(self):
        while self._isAlive:
            try:
                self.acceptConnection()
            except socket.timeout as e:
                logger.debug("socket.timeout: %s" % e)
                continue
            except Exception as e:
                logger.exception(e)
                continue

            while self._isAlive:
                try:
                    obj = self.readObj()
                    self._processMessage(obj)
                except socket.timeout as e:
                    logger.debug("socket.timeout: %s" % e)
                    self.stop()
                    continue
                except Exception as e:
                    logger.exception(e)
                    self._closeConnection()
                    break

    def start(self):
        self._isAlive = True
        super(ThreadedServer, self).start()

    def stop(self):
        self._isAlive = False
