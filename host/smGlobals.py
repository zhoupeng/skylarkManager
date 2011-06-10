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

spice_base_port = SPICE_BASE_PORT
def get_free_port():
    global spice_base_port
    spice_base_port = spice_base_port + 1
    return spice_base_port - 1

