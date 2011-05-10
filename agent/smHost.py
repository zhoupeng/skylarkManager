#!/usr/bin/env python
#
# Filename: agent/smHost.py
#
# -------------------------------------------------------------------
#
# 
#
# -------------------------------------------------------------------
import libconf

import socket
from smCMD import *
import smErrors
import threading


class Host(threading.Thread):
    """ Present a host node
    """
    def __init__(self, sock = None, addr = None, type = None):
        """
        @type type: string
        @param type: hypervisor type
        @type sock: socket
        @param sock: host end of socket between agent and host
        @type addr:
        @param addr: the address bound to the socket on the other end of the 
        connection.
        """
        threading.Thread.__init__(self)

        print "HOST constructor"
        self.sock = sock
        self.type = type
        self.addr = addr
        self.ready = False

    def init(self, sock, addr, type):
        if (not sock or not addr or not type):
            raise smErrors.GenericError("parameter shouldn't be NULL:[sock=%s,"
                                        "addr=%s, type=%s]" % (sock, addr, type))

        print "host_init"
        self.sock = sock
        self.type = type
        self.addr = addr
        self.ready = False
        self.ready = True

    # Thread function serves the host.
    def run(self):
        if (not self.ready):
            raise smErrors.ProgrammerError("host initialization is "
                                           "needed before host thread run.")

        while True:
            data = self.sock.recv(128)
            if data:
                print data
                self.sock.send(data)


