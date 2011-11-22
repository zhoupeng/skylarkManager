#!/usr/bin/env python
#
# Filename: host/smKVM.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
import libconf

from CONSTANTS import *
import smBase
import os

class KVMNode(smBase.BaseHypervisor):

    def getType(self):
        return KVM_TYPE

    def getCPUUsage(self):
        """Get the cpu usage.

        @return: a dict with the following keys:
         - cpusec: the cpu consumed in milliseconds in the measure interval
         - cpurate: the cpu usage percentage in the measure interval
        """
        return self.getLinuxCPUUsage()

    def getNodeInfo(self):
        """Return information about the node.

        @return: a dict with the following keys (memory values in MiB):
            - memory_total: the total memory size on the node
            - memory_free: the available memory on the node for instances
            - memory_dom0: the memory used by the node itself, if available
            - nr_cpus(cpu_total): total number of CPUs
            - nr_nodes(cpu_nodes): in a NUMA system, the number of domains
            - nr_sockets(cpu_sockets): the number of
                                       physical CPU sockets in the node

        """
        return self.getLinuxNodeInfo()

    def createInstance(self, vmName, spicehost, spiceport,
                       memory = 300):
        """Create a VM
        """
        pass

    def newInstanceBySnapshot(self, vmName, spicehost, spiceport):
        """Create a VM from checkpoint template file
        Use our storage system to parse vmName
        """
        pass

    def restoreInstance(self, vmName, spicehost, spiceport):
        """Restore a VM from it's own checkpoint file
        Don't use and allow the storage system to parse vmName, keep
        the same as you see.
        Assume the vm's checkpoint file is saved before

        @type vmName: str
        @param vmName: the actual name of an instance
        @type spicehost: str
        @param spicehost: This host's ip for this spice server
        @type spiceport: int
        @param spiceport: the port for this spice server
        """
        pass

    def shutdownInstance(self, instanceid):
        """ shutdown the vm instance (instanceid)

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """

    def saveInstance(self, instanceid):
        """ save the vm instance (instanceid)

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """

    def verify(self):
        """Verify the hypervisor.

        Check that the binary exists.

        """
        raise NotImplementedError
        #if not os.path.exists(constants.KVM_PATH):
        #    return "The kvm binary ('%s') does not exist." % constants.KVM_PATH
        #if not os.path.exists(constants.SOCAT_PATH):
        #    return "The socat binary ('%s') does not exist." % constants.SOCAT_PATH

