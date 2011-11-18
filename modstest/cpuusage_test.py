#!/usr/bin/env python
#
# Filename: modstest/cpuusage_test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
""" test lib/smCPUUsage.py
"""
import libconf

from smCPUUsage import CPUsage

cpuu = CPUsage(0.2)
i = 3
while i:
    print cpuu
    cpuu.recompute()
    i -= 1
