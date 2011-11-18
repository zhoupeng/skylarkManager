#!/usr/bin/env python
#
# Filename: host/smBase.py
#
# Based on ganeti hv_base.py
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
# Copyright (C) 2006, 2007, 2008, 2009, 2010 Google Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.


"""Base class for all hypervisors
NB. The XenNode is not from this class because of great difference.

"""
import libconf

import os
import re
import logging

import smErrors as errors
import smProcess as utilsProcess
import smIO
import smCPUUsage

class BaseHypervisor(object):
    """Abstract virtualisation technology interface
 
    The goal is that all aspects of the virtualisation technology are
    abstracted away from the rest of code.
    """
 
    def __init__(self):
        pass
 
    def startInstance(self, instance, block_devices, startup_paused):
        """Start an instance."""
        raise NotImplementedError
 
    def stopInstance(self, instance, force=False, retry=False, name=None):
        """Stop an instance
       
        @type instance: L{objects.Instance}
        @param instance: instance to stop
        @type force: boolean
        @param force: whether to do a "hard" stop (destroy)
        @type retry: boolean
        @param retry: whether this is just a retry call
        @type name: string or None
        @param name: if this parameter is passed, the the instance object
            should not be used (will be passed as None), and the shutdown
            must be done by name only
       
        """
        raise NotImplementedError
 
    def cleanupInstance(self, instance_name):
        """Cleanup after a stopped instance
       
        This is an optional method, used by hypervisors
        that need to cleanup after an instance has been stopped.
       
        @type instance_name: string
        @param instance_name: instance name to cleanup after
       
        """
        pass
 
    def rebootInstance(self, instance):
        """Reboot an instance."""
        raise NotImplementedError
 
    def listInstances(self):
        """Get the list of running instances."""
        raise NotImplementedError
 
    def getInstanceInfo(self, instance_name):
        """Get instance properties.
       
        @type instance_name: string
        @param instance_name: the instance name
       
        @return: tuple (name, id, memory, vcpus, state, times)
       
        """
        raise NotImplementedError
 
    def getAllInstancesInfo(self):
        """Get properties of all instances.
       
        @return: list of tuples (name, id, memory, vcpus, stat, times)
       
        """
        raise NotImplementedError
 
    def getNodeInfo(self):
        """Return information about the node.
       
        @return: a dict with the following keys (values in MiB):
            - memory_total: the total memory size on the node
            - memory_free: the available memory on the node for instances
            - memory_dom0: the memory used by the node itself, if available
       
        """
        raise NotImplementedError
 
    @classmethod
    def getInstanceConsole(cls, instance, hvparams, beparams):
        """Return information for connecting to the console of an instance.
       
        """
        raise NotImplementedError
 
    def verify(self):
        """Verify the hypervisor.
       
        """
        raise NotImplementedError
 
    @classmethod
    def powercycleNode(cls):
        """Hard powercycle a node using hypervisor specific methods.
       
        This method should hard powercycle the node, using whatever
        methods the hypervisor provides. Note that this means that all
        instances running on the node must be stopped too.
       
        """
        raise NotImplementedError
 
    @staticmethod
    def getLinuxNodeInfo():
        """For linux systems, return actual OS information.
       
        This is an abstraction for all non-hypervisor-based classes, where
        the node actually sees all the memory and CPUs via the /proc
        interface and standard commands. The other case if for example
        xen, where you only see the hardware resources via xen-specific
        tools.
       
        @return: a dict with the following keys (values in MiB):
              - memory_total: the total memory size on the node
              - memory_free: the available memory on the node for instances
              - memory_dom0: the memory used by the node itself, if available
              - nr_cpus: total number of CPUs
              - nr_nodes: in a NUMA system, the number of domains
              - nr_sockets: the number of physical CPU sockets in the node
       
        """
        try:
            data = smIO.ReadFile("/proc/meminfo").splitlines()
        except EnvironmentError, err:
            raise errors.HypervisorError(
                      "Failed to list node info: %s" % (err,))
       
        result = {}
        sum_free = 0
        try:
            for line in data:
                splitfields = line.split(":", 1)
               
                if len(splitfields) > 1:
                    key = splitfields[0].strip()
                    val = splitfields[1].strip()
                    if key == "MemTotal":
                        result["memory_total"] = int(val.split()[0]) / 1024
                    elif key in ("MemFree", "Buffers", "Cached"):
                        sum_free += int(val.split()[0]) / 1024
                    elif key == "Active":
                        result["memory_dom0"] = int(val.split()[0]) / 1024
        except (ValueError, TypeError), err:
            raise errors.HypervisorError(
                             "Failed to compute memory usage: %s" % (err,))
        result["memory_free"] = sum_free
       
        cpu_total = 0
        try:
            fh = open("/proc/cpuinfo")
            try:
                cpu_total = len(re.findall(
                             "(?m)^processor\s*:\s*[0-9]+\s*$", fh.read()))
            finally:
                fh.close()
        except EnvironmentError, err:
            raise errors.HypervisorError(
                                   "Failed to list node info: %s" % (err,))
        result["cpu_total"] = cpu_total
        # FIXME: export correct data here
        result["cpu_nodes"] = 1
        result["cpu_sockets"] = 1
       
        return result

    @staticmethod
    def getLinuxCPUUsage():
        """For Linux systems, return actual cpu usage
        including percentage and milliseconds.

        The usage is calculated via /proc interface

        @return: a dict with the following keys:
         - cpusec: the cpu consumed in milliseconds in the measure interval
         - cpurate: the cpu usage percentage in the measure interval
        """
        cpuu = smCPUUsage.CPUsage()

        cpuusage = {'cpurate': cpuu.getcpurate(),
                    'cpusec': cpuu.getcpusec()}

        return cpuusage
 
    @classmethod
    def linuxPowercycle(cls):
        """Linux-specific powercycle method.
       
        """
        try:
            fd = os.open("/proc/sysrq-trigger", os.O_WRONLY)
            try:
                # try to reboot the machine by trigger SysRq handler
                # provided by CONFIG_MAGIC_SYSRQ module kernel module.
                # Equal to the key combination Alt + SysRq + B
                os.write(fd, "b")
            finally:
                os.close(fd)
        except OSError:
            logging.exception("Can't open the sysrq-trigger file")
            result = utilsProcess.RunCmd(["reboot", "-n", "-f"])
            if not result:
                logging.error("Can't run shutdown: %s", result.output)

