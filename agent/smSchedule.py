#!/usr/bin/env python
#
# Filename: agent/smSchedule.py
# Sched framework
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.05 ~
#
# -------------------------------------------------------------------
""" Three steps to add your own sched method:
1. Add your sched method to Scheduler
2. Give a string name for your sched method
3. Add an item to Scheduler.__sched_method_map based on step 1&2
"""

import libconf
from smGlobals import *

class Scheduler:
    """scheduler
    You can add your own schedule method here,
    Then you only need to call setMethod(your_own)
    to take effect. 

    This class is single mode, you should always get an instance through
    Scheduler.getInstance().

    The singleton variable is part of the class, 
    and therefore common among all instances. 
    We can refer to it either as self.singleton or as Scheduler.singleton. 
    Each subclass must have this declaration.
    Refering to 'Python Singleton Class' from
    http://homepage.mac.com/s_lott/books/oodesign/htmlchunks/ch17s05.html
    """
    singleton = None

    M_CYCLIC = 'cyclic'
    M_CPU = 'cpu'
    M_MEM = 'mem'
    M_CPU_MEM = 'cpu_mem'
    M_MEM_CPU = 'mem_cpu'
    # Define a proper name for your sched method here.
    M_DEFAULT = 'default'

    __method = M_DEFAULT
    __sched_method_map = {}

    def __init__(self):

        self.__sched_method_map = { Scheduler.M_CYCLIC: self.__cyclic,
                         Scheduler.M_CPU: self.__cpu,
                         Scheduler.M_MEM: self.__memory,
                         Scheduler.M_CPU_MEM: self.__cpu_mem,
                         Scheduler.M_MEM_CPU: self.__mem_cpu, 
                         # Add a new table item for
                         # your own sched method here.
                         Scheduler.M_DEFAULT: self.__cyclic }

        self.__method = Scheduler.M_DEFAULT 

    @staticmethod
    def getInstance():
        """ You should always get a Scheduler's instance through this interface,
        to keep there is only one Scheduler instance through the whole system.
        """
        if Scheduler.singleton:
            return Scheduler.singleton
        else:
            Scheduler.singleton = Scheduler()
            return Scheduler.singleton

    def setMethod(self, method, *args, **kwargs):
        """ set the current sched method
        @type method: str
        @param method: method name
        @type args: list
        @param args: reserved for sched method needing extra info.
        @type kwargs: dict
        @param kwargs: reserved for sched method needing extra info.
        """

        ret = True
        if method in self.__sched_method_map.keys():
            self.__method = method
            self.args = args
            self.kwargs = kwargs
        else:
            print """Sched Method: %s is not supported
 Keep to use current method: %s""" % (method, self.getMethod())
            ret = False
        
        return ret

    def getMethod(self):
        """ Get the current method.
        """
        return self.__method 

    def schedule(self, hosts):
        """ Determine the node to schedule

        @type hosts: HostsStruct
        @param hosts: All of the hosts joined
        """
        node = None

        hosts.lock()
        try:
            print self.__sched_method_map[self.__method]
            node = self.__sched_method_map[self.__method](hosts.nodes)
        finally:
            hosts.unlock()

        return node

    def __cyclic(self, nodes):
        """ cyclic schedule 

        @type nodes: list
        @param nodes: The list of nodes
        """
        pass

    def __memory(self, nodes):
        """ schedule by mem

        @type nodes: list
        @param nodes: The list of nodes
        """
        nodes.sort(key = lambda n: n.latestReport['memory_dom0'] +
                                   n.latestReport['memory_free'],
                                   reverse = True)
        return nodes[0]

    def __cpu(self, nodes):
        """ schedule by cpu 

        @type nodes: list
        @param nodes: The list of nodes
        """
        # FIXME: How to get MIPS effectively?
        # MIPS is more reasonable than cpu frequency.
        nodes.sort(key = lambda n: (1 - n.latestReport['cpurate'] / 100) *
                                    n.basicInfo['cpu_mhz'],
                                    reverse = True)
        return nodes[0]

    def __mem_cpu(self, nodes):
        """ schedule by men&&cpu, mem first.

        @type nodes: list
        @param nodes: The list of nodes
        """

        if self.__cpu(nodes):
            return self.__memory(nodes)
        return None

    def __cpu_mem(self, nodes):
        """ schedule by cpu&&mem, cpu first.

        @type nodes: list
        @param nodes: The list of nodes
        """

        if self.__memory(nodes):
            return self.__cpu(nodes)
        return None

    # Add your own sched method here
    # def __yourmethod(self, ...)

