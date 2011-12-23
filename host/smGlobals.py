#!/usr/bin/env python
#
# Filename: host/smGlobals.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
#
# -------------------------------------------------------------------
import libconf

from CONSTANTS import *
import smList
import socket

# instances
instances = smList.LockList()

spice_port_current = SPICE_BASE_PORT
def get_free_port4spice():
    global spice_port_current

    if not spice_port_current % (SPICE_BASE_PORT + SPICE_PORT_RANGE + 1):
        spice_port_current = SPICE_BASE_PORT

    while True:
        spice_port_current += 1
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('', spice_port_current - 1))
            s.close()
            break
        except Exception, msg:
            print "%s: will test next port" % msg
            continue

    return spice_port_current - 1

