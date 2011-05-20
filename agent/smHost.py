#!/usr/bin/env python
#
# Filename: agent/smHost.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
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
    __uuid = None

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
            cmd = self.sock.recv(1024)
            if cmd:
                jsobj = json.loads(cmd)

                if jsobj[0] == CMDHostAgent.join:
                    if not self.__uuid:
                        self.__uuid = jsobj[1]['uuid']
                        self.type = jsobj[1]['type']
                        self.sock.send(CMDHostAgent.ack_join(self.__uuid, True))
                    else:
                        print("Unexpected data received: %s: the host login req send again.", cmd)
                        self.sock.send(CMDHostAgent.ack_join(self.__uuid, False))
                        continue
                elif jsobj[0] == CMDHostAgent.rsreport:
                    print jsobj


