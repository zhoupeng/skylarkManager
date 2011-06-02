#!/usr/bin/env python
#
# Filename: agent/smClient.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
#
# -------------------------------------------------------------------
from smGlobals import *
import threading
import simplejson as json
from smSchedule import Scheduler
import socket
from smCMD import *

class ClientReq:
    """ represent a request from the client
    """

    # TODO
    # extend the type param
    # add management interface

    def __init__(self, senderaddr, type):
        """ need to rewrite to describe more complicated req.
        @type senderaddr: tuple
        @param senderaddr: (host, port)
        @type type: str
        @param type: instance type, used temporarily, need to be modified
        """
        self.senderaddr = senderaddr
        self.type = type

class Client(threading.Thread):
    """ Deal with all the reqs from the clients.
    Client reqs here are authenticated by the webfront,
    so the comming reqs are assumed valid.

    The work of this class:
    1) This class receive req from client routing from the webfront,
    2) buffer the req in pendingReqsFromCli
    3) Schedule the req to a host

    Note, this class don't wait for the response from the host
    """
    def __init__(self, port, host = ''):
        """
        @type port: int
        @param port: the udp port binded 
        """
        threading.Thread.__init__(self)

        self.port = port
        self.host = host
        self.sock = socket.socket(type = socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.running = True
        self.sched = Scheduler.getInstance()

    def run(self):
        """ Thread body
        """
        while self.running:

            global hosts
            global pendingReqsFromCli

            # The return value is a pair (string, address)
            # where string is a string representing the data received and
            # address is the address of the socket sending the data.
            # here is (host, port)
            data, senderaddr = self.sock.recvfrom(512)

            if not data:
                continue
            
            jsobj = json.loads(data)
            print "ClientSrv receive: %s" % jsobj

            # Add a pending req to pendingReqsFromCli queue
            clireq = ClientReq(senderaddr, jsobj[1]['type'])
            pendingReqsFromCli.lock()
            pendingReqsFromCli.append(clireq)
            pendingReqsFromCli.unlock()

            if jsobj[0] == CMDClientAgent.reqinstance:
                h = self.sched.schedule(hosts)

                if not h:
                    print "Client: error, scheded h is None"
                    continue

                reqins2host = CMDHostAgent.cmd_reqinstance(h.getUUID(),
                                                           type = clireq.type)
                h.sock.send(reqins2host)

