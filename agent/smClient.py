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
    """ represent a request from the webfront client
    """

    # TODO
    # add management interface

    def __init__(self, senderaddr, request):
        """ The requester's address and request
        
        @type senderaddr: tuple
        @param senderaddr: (host, port)
        @type request: python object to present a request
        @param request: request cmd and releated parameters, for detail
        of request, pls see common/smCMD.CMDClientAgent 
        """
        self.senderaddr = senderaddr
        self.request = request

class Client(threading.Thread):
    """ Deal with all the reqs from the clients.
    Client reqs here are authenticated by the webfront,
    so the coming reqs are assumed valid.

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
            data, senderaddr = self.sock.recvfrom(1024)

            if not data:
                continue

            # If the received json is in syntax err, continue.
            try:
                jsobj = json.loads(data)
            except JSONDecodeError, e:
                print e
                print "ClientSrv receive: %s" % data
                continue

            print "ClientSrv receive: %s" % jsobj

            # Add a pending req to pendingReqsFromCli queue
            clireq = ClientReq(senderaddr, jsobj)
            pendingReqsFromCli.lock()
            pendingReqsFromCli.append(clireq)
            pendingReqsFromCli.unlock()

            if jsobj[0] == CMDClientAgent.createinstance:
                h = self.sched.schedule(hosts)

                if not h:
                    print "Client: error, scheded h is None"
                    continue

                req2host = CMDHostAgent.cmd_createInstance(h.getUUID(),
                                                              jsobj[1]['owner'],
                                                              jsobj[1]['type'],
                                                              jsobj[1]['nth'])
                h.sock.send(req2host)
            elif jsobj[0] == CMDClientAgent.newinstancebysnapshot:
                h = self.sched.schedule(hosts)

                if not h:
                    print "Client: error, scheded h is None"
                    continue

                req2host = CMDHostAgent.cmd_newInstanceBySnapshot(h.getUUID(),
                                                              jsobj[1]['owner'],
                                                              jsobj[1]['type'],
                                                              jsobj[1]['nth'])
                h.sock.send(req2host)
            elif jsobj[0] == CMDClientAgent.shutdowninstance:
                h = self.sched.schedule(hosts, hostuuid = jsobj[1]['hostuuid'])

                if not h:
                    print "Client: error, scheded h is None"
                    continue

                req2host = CMDHostAgent.cmd_shutdownInstance(h.getUUID(),
                                                             jsobj[1]['owner'],
                                                             jsobj[1]['type'],
                                                             jsobj[1]['nth'])
                h.sock.send(req2host)
            elif jsobj[0] == CMDClientAgent.restoreinstance:
                h = self.sched.schedule(hosts, hostuuid = jsobj[1]['hostuuid'])

                if not h:
                    print "Client: error, scheded host is None"
                    continue

                req2host = CMDHostAgent.cmd_restoreInstance(h.getUUID(),
                                                            jsobj[1]['owner'],
                                                            jsobj[1]['type'],
                                                            jsobj[1]['nth'])
                h.sock.send(req2host)
            elif jsobj[0] == CMDClientAgent.saveinstance:
                h = self.sched.schedule(hosts, hostuuid = jsobj[1]['hostuuid'])

                if not h:
                    print "Client: error, scheded host is None"
                    continue

                req2host = CMDHostAgent.cmd_saveInstance(h.getUUID(),
                                                         jsobj[1]['owner'],
                                                         jsobj[1]['type'],
                                                         jsobj[1]['nth'])
                h.sock.send(req2host)
