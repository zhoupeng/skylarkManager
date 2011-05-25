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

# hosts
class HostsStruct:
    def __init__(self):
        self.nodes = []
        self.lock = threading.Lock()

hosts = HostsStruct()
