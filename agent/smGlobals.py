#!/usr/bin/env python
#
# Filename: agent/smGlobals.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------
import threading
import smDump

class LockList:
    """ Wraper of List with lock
    """
    def __init__(self):
        self.nodes = []
        self.__lock = threading.Lock()

    def lock(self):
        self.__lock.acquire()
    
    def unlock(self):
        self.__lock.release()

    def append(self, node):
        self.nodes.append(node)

    def dump(self):
        print "Dump nodes of LockList:"
        print self.nodes
        #smDump.dumpObj(self)
        #for n in self.nodes:
            #n.dump()

# hosts
hosts = LockList()

# Pending reqs from clients
pendingReqsFromCli = LockList()
