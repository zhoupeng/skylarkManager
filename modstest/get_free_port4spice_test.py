#!/usr/bin/env python
#
# Filename: modstest/get_free_port4spice_test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.12 ~
#
# -------------------------------------------------------------------
"""test host/smGlobals.py:get_free_port4spice
"""
import libconf
from smGlobals import *
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 6200))
print get_free_port4spice()
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('', 6201))
