#!/usr/bin/env python
#
# Filename: common/CONSTANTS.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------
from smSettings import *

# How long to report host resource once
RS_REPORT_INTERVAL = 30 # seconds

# host types
XEN_TYPE = 'xen'
KVM_TYPE = 'kvm'

# spice
SPICE_HOST = 'localhost' # or ip interface, e.g. 192.168.1.187
SPICE_BASE_PORT = 6200 # port is local to the host
SPICE_PORT_RANGE = 5000
