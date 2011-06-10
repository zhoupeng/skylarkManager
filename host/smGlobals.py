#!/usr/bin/env python
#
# Filename: host/smHost.py
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

# instances
instances = smList.LockList()

spice_port_current = SPICE_BASE_PORT
def get_free_port4spice():
    global spice_port_current

    if not spice_port_current % (SPICE_BASE_PORT + SPICE_PORT_RANGE + 1):
        spice_port_current = SPICE_BASE_PORT

    spice_port_current += 1
    return spice_port_current - 1

