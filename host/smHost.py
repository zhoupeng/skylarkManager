#!/usr/bin/env python
#
# Filename: host/smHost.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------
import libconf

import smNet
import socket
import smErrors as errors
import smXen
from smCMD import *
import smIO
import simplejson as json

class Host(object):
    """
    @type uuid: str
    @param uuid: the uuid of this host node, readonly
    """

    def __init__(self, aggentIP, aggentPort, pool = ''):
        if (smNet.IPAddress.getAddressFamily(aggentIP) == socket.AF_INET):
            self.aggentAddr = smNet.IP4Address(aggentIP)
        elif (smNet.IPAddress.getAddressFamily(aggentIP) == socket.AF_INET6):
            self.aggentAddr = smNet.IP6Address(aggentIP)
        else:
            raise errors.IPAddressError("IP Address %s invalid" % aggentIP)

        # Standard Port NO. is in [0, 65535], but we exclude the two ends
        if (aggentPort > 0 and aggentPort < 65535):
            self.aggentPort = aggentPort
        else:
            raise errors.PortError("Port number:%d is invalid." % aggentPort)

        self.sock = socket.socket(type = socket.SOCK_STREAM)
        self.node = smXen.XenNode()
        self.__uuid = smIO.NewUUID()

    def getType(self):
        """ get the type of this host node
        """
        return self.node.getType()

    def getUUID(self):
        """ get the uuid of this host node.
        """
        return self.__uuid

    def join(self):
        """join in the cluster
        """
        # sockaddr is tuple
        ag = (self.aggentAddr.address, self.aggentPort)
        self.sock.connect(ag)

        # host join req to agent.
        self.sock.send(CMDHostAgent.cmd_join(self.getUUID(), self.getType()))

        ack = self.sock.recv(128)
        while not ack:
            ack = self.sock.recv(128)
        ackobj = json.loads(ack)
        if (ackobj[0] == CMDHostAgent.join and 
                        ackobj[1]['uuid'] == self.getUUID()):
            return ackobj[1]['succeed']
        raise errors.RemoteError("Unexpected data received:%s", ack);

    def leave(self):
        """leave the cluster
        """
        pass
