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

    __method = Scheduler.M_DEFAULT

    sched_method_map = { Scheduler.M_CYCLIC: Scheduler.__cyclic,
                         Scheduler.M_CPU: Scheduler.__cpu,
                         Scheduler.M_MEM: Scheduler.__mem,
                         Scheduler.M_CPU_MEM: Scheduler.__cpu_mem,
                         Scheduler.M_MEM_CPU: Scheduler.__mem_cpu, 
                         # Add a new table item for your own sched method here.
                         Scheduler.M_DEFAULT: Scheduler.__cyclic }

    def __init__(self):
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

    def setMethod(self, method, *args = None, **kwargs = None):
        """ set the current sched method
        @type method: str
        @param method: method name
        @type args: list
        @param args: reserved for sched method needing extra info.
        @type kwargs: dict
        @param kwargs: reserved for sched method needing extra info.
        """

        ret = True
        if method in Scheduler.sched_method_map.keys():
            self.__method = method
            self.args = args
            self.kwargs = kwargs
        else:
            print "Sched Method: %s is not supported\n"
                  "Keep to use current method: %s"
                   % (method, self.getMethod())
            ret = False
        
        return ret

    def getMethod(self):
        """ Get the current method.
        """
        return __method 

    def schedule(self, hosts):
        """ Determine the node to schedule

        @type hosts: HostsStruct
        @param hosts: All of the hosts joined
        """
        node = None

        hosts.lock.acquire()
        try:
            node = self.sched_method_map[self.__method](hosts.nodes)
        finally:
            hosts.lock.release()

        return node

    @staticmethod
    def __cyclic(nodes):
        """ cyclic schedule 

        @type nodes: list
        @param nodes: The list of nodes
        """
        pass

    @staticmethod
    def __memory(nodes):
        """ schedule by mem

        @type nodes: list
        @param nodes: The list of nodes
        """
        pass

    @staticmethod
    def __cpu(nodes):
        """ schedule by cpu 

        @type nodes: list
        @param nodes: The list of nodes
        """
        pass

    @staticmethod
    def __mem_cpu(nodes):
        """ schedule by men&&cpu, mem first.

        @type nodes: list
        @param nodes: The list of nodes
        """

        pass

    @staticmethod
    def __cpu_mem(nodes):
        """ schedule by cpu&&mem, cpu first.

        @type nodes: list
        @param nodes: The list of nodes
        """
        pass

    # Add your own sched method here

