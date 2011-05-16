#!/usr/bin/env python
#
# Filename: agent/smListeners.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------
import libconf

import socket
import threading
import smHost
from smGlobals import *
from CONSTANTS import *

def hostlistener(listener):
    """Listen to host connection.
    """
    listener.sock.listen(5)

    while True:
        global hostList
        connSock, addr = listener.sock.accept()

        h = smHost.Host()
        h.init(connSock, addr, XENHOST)
        # insert into the hostlist
        hostList.append(h)
        h.start()
        #h.join()
        print "hostlistener(): %s " % h
        #h = None


def clientlistener(listener):
    """Listen to client connection.
    """
    pass


def agentlistener(listener):
    """Listen to agent connection.
    """
    pass


listenhandlers = {
    "host" : hostlistener,
    "client" : clientlistener,
    "agent" : agentlistener
    }

class Listener(threading.Thread):
    """ listen to socket's client connect request.
    """
    def __init__(self, port, type, host = ''):
        """ 
        @type host: string
        @param host: server interface to bind, default all available interfaces
        @type port: int
        @param port: server port to bind
        @type type: the purpose of this listener(host, client or other agent)
        """
        threading.Thread.__init__(self)

        self.host = host
        self.port = port
        self.type = type
        self.sock = socket.socket(type = socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
    
    def run(self):
        listenhandlers[self.type](self)

