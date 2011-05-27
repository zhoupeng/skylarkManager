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
import smDump


class Host(threading.Thread):
    """ Present a host node
    @type ready: bool
    @param ready: If this host is initialized
    @type latestReport: dict
    @param latestReport: the latest resource report from the host.
    @type basicInfo: dict
    @param basicInfo: the basic info of host(cpu hard & total mem)
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
        self.latestReport = {}
        self.basicInfo = {}

    def init(self, sock, addr, type):
        if (not sock or not addr or not type):
            raise smErrors.GenericError("parameter shouldn't be NULL:[sock=%s,"
                                        "addr=%s, type=%s]" % (sock, addr, type))

        print "host_init"
        self.sock = sock
        self.type = type
        self.addr = addr
        self.ready = True

    # Thread function serves the host.
    def run(self):
        if (not self.ready):
            raise smErrors.ProgrammerError("host initialization is "
                                           "needed before host thread run.")

        while self.ready:
            cmd = self.sock.recv(1024)
            if cmd:
                jsobj = json.loads(cmd)

                if jsobj[0] == CMDHostAgent.join:
                    if not self.__uuid:
                        self.__uuid = jsobj[1]['uuid']
                        self.type = jsobj[1]['type']
                        self.basicInfo.update(memory_total = jsobj[1]['memory_total'],
                               cpu_mhz = jsobj[1]['cpu_mhz'],
                               cpu_total = jsobj[1]['cpu_total'],
                               cpu_nodes = jsobj[1]['cpu_nodes'],
                               cores_per_socket = jsobj[1]['cores_per_socket'],
                               threads_per_core = jsobj[1]['threads_per_core'],
                               cpu_sockets = jsobj[1]['cpu_sockets'])
                        self.latestReport.update(cpurate = jsobj[1]['cpurate'],
                                memory_free = jsobj[1]['memory_free'],
                                memory_dom0 = jsobj[1]['memory_dom0'])
                        print self.basicInfo
                        print self.latestReport
                        self.sock.send(CMDHostAgent.ack_join(self.__uuid, True))
                    else:
                        print("Unexpected data received: %s: the host "
                              "login req send again.", cmd)
                        self.sock.send(CMDHostAgent.ack_join(self.__uuid, False))
                        continue
                elif jsobj[0] == CMDHostAgent.rsreport:
                    self.latestReport.update(jsobj[1])
                    print self.latestReport

    def dump(self):
        smDump.dumpObj(self)
