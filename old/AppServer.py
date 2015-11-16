#!/usr/bin/python

import ThreadedServer


class AppServer(ThreadedServer.ThreadedServer):
    def __init__(self):
        self.timeout = 30.0

    def _processMessage(self, obj):
        """ virtual method """
        if obj != '':
            if obj['message'] == "new connection":
                pass

if __name__ == '__main__':
    c = AppServer()
    print "Starting appserver at %s:%s"%(c._get_address(), c._get_port())
    p = c._get_port()
    ip = c._get_address()
    print "Starting appserver at %s:%s"%(ip, p)

    c.start()
