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
import threading
import smTimer
from CONSTANTS import *
from smGlobals import *
import smObjects
import smLog
import sys
from smTypes import *

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
        # periodical resource reporter
        self.rsReporter = None
        # thread to response to command from agent.
        self.agentCMDThread = None
        self.running = False

    def getType(self):
        """ get the type of this host node
        """
        return self.node.getType()

    def getUUID(self):
        """ get the uuid of this host node.
        """
        return self.__uuid

    def joinIn(self):
        """join in the cluster
        rename join with joinIn to avoid mixing up with Thread.join
        """
        # sockaddr is tuple
        ag = (self.aggentAddr.address, self.aggentPort)
        self.sock.connect(ag)

        cpuuse = self.node.getCPUUsage()
        nodeinfo = self.node.getNodeInfo()
        misc = {}
        misc.update(cpuuse, **nodeinfo)
        misc.update(type = self.getType())
        del misc['cpusec']
        # host join req to agent, ** used for keyword args(that is dict)
        self.sock.send(CMDHostAgent.cmd_join(self.getUUID(), **misc))

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

    def start(self):
        self.running = True
        # periodical resource reporter
        self.rsReporter = smTimer.BackgroundTask(RS_REPORT_INTERVAL, 
                                                 Host._resourceReport, [self])
        self.agentCMDThread = AgentCMDThread(self)
        self.agentCMDThread.start()
        self.rsReporter.start()
        self.agentCMDThread.join()

    @staticmethod
    def _resourceReport(host):
        """ The timer function of rsReporter.
        """

        if not host.running:
            host.rsReporter.cancel()
            return

        cpuuse = host.node.getCPUUsage()
        nodeinfo = host.node.getNodeInfo()

        report = {}
        report.update(cpurate = cpuuse['cpurate'],
                      memory_free = nodeinfo['memory_free'],
                      memory_dom0 = nodeinfo['memory_dom0'])
        # send resource report, ** used for keyword args(that is dict)
        host.sock.send(CMDHostAgent.cmd_rsreport(host.getUUID(), **report))


class AgentCMDThread(threading.Thread):
    """ thread to response to command from agent.
    """

    def __init__(self, host):
        """
        @type host: Host
        @parem host: the served host
        """
        threading.Thread.__init__(self)

        self.host = host

    def run(self):
        while self.host.running:
            cmd = self.host.sock.recv(1024)
            if cmd:
                jsobj = json.loads(cmd)
                print "host:AgentCMDThread receive: %s" % jsobj
                
                if jsobj[0] == CMDHostAgent.createinstance:
                    if self.host.getUUID() != jsobj[1]['uuid']:
                        # ignore reqs shouldn't to me
                        continue 
                    else:
                        hip = smNet.IPAddress.get_ip_address_nic(SPICE_NI)

                        if not hip:
                            print "Fail to get ip of NI(%s):%s:%s" % (SPICE_NI, __file__,
                            smLog.__function__())
                            sys.exit()

                        hport = get_free_port4spice()
                        # The format of instanceid(vm name) here are only useful
                        # to our storage system to share a single disk img
                        # file by @type, otherwise it only need to keep unique
                        # The order puting 'type' at the end to help our
                        # storage system to access in convenience.
                        instanceid = jsobj[1]['owner'] + jsobj[1]['nth']
                                     + '@' + jsobj[1]['type']

                        inst = self.host.node.createInstance(instanceid, hip,
                                                        hport)

                        ackcreateins = None
                        if inst:
                            global instances
                            inst.owner = jsobj[1]['owner']
                            inst.type = jsobj[1]['type']
                            inst.nth = jsobj[1]['nth']
                            instances.lock()
                            instances.append(inst)
                            instances.unlock()
                            ackcreateins = CMDHostAgent.ack_createInstance(
                                         self.host.getUUID(),
                                         status = Status.SUCCESS,
                                         msg = 'create an instance successfully',
                                         owner = inst.owner,
                                         type = inst.type,
                                         nth = inst.nth,
                                         spicehost = inst.spicehost,
                                         spiceport = inst.spiceport)
                        else:
                            print "AgentCMDThread: createInstance failed"
                            ackcreateins = CMDHostAgent.ack_createInstance(
                                           self.host.getUUID(),
                                           status = Status.FAIL,
                                           msg = 'failed to create an instance',
                                           owner = jsobj[1]['owner'],
                                           type = jsobj[1]['type'],
                                           nth = jsobj[1]['nth'],
                                           spicehost = '',
                                           spiceport = 0)

                        self.host.sock.send(ackcreateins)

                elif jsobj[0] == CMDHostAgent.newinstancebysnapshot:
                    if self.host.getUUID() != jsobj[1]['uuid']:
                        # ignore reqs shouldn't to me
                        continue 

                    hip = smNet.IPAddress.get_ip_address_nic(SPICE_NI)

                    if not hip:
                        print "Fail to get ip of NI(%s):%s:%s" % (SPICE_NI, __file__,
                        smLog.__function__())
                        sys.exit()

                    hport = get_free_port4spice()
                    # The format of instanceid(vm name) here are only useful
                    # to our storage system to share a single disk img
                    # file by @type, otherwise it only need to keep unique
                    # The order puting 'type' at the end to help our
                    # storage system to access in convenience.
                    instanceid = jsobj[1]['owner'] + jsobj[1]['nth']
                                 + '@' + jsobj[1]['type']
                                 + '@' + '%s' % spicehost
                                 + '@' + '%s' % spiceport

                    inst = self.host.node.newInstanceBySnapshot(instanceid,
                                                                hip,
                                                                hport)

                    acknewins = None
                    if inst:
                        global instances
                        inst.owner = jsobj[1]['owner']
                        inst.type = jsobj[1]['type']
                        inst.nth = jsobj[1]['nth']
                        instances.lock()
                        instances.append(inst)
                        instances.unlock()
                        acknewins = CMDHostAgent.ack_newInstanceBySnapshot(
                          self.host.getUUID(),
                          status = Status.SUCCESS,
                          msg = 'create instance by snapshot successfully',
                          owner = inst.owner,
                          type = inst.type,
                          nth = inst.nth,
                          spicehost = inst.spicehost,
                          spiceport = inst.spiceport)
                    else:
                        print "AgentCMDThread: createInstance  by snapshot failed"
                        acknewins = CMDHostAgent.ack_newInstanceBySnapshot(
                                       self.host.getUUID(),
                                       status = Status.FAIL,
                                       msg = 'failed to create instance by snapshot',
                                       owner = jsobj[1]['owner'],
                                       type = jsobj[1]['type'],
                                       nth = jsobj[1]['nth'],
                                       spicehost = '',
                                       spiceport = 0)

                    self.host.sock.send(acknewins)


