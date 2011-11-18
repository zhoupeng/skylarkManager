#!/usr/bin/env python
#
# Filename: modstest/baseHypervisor_test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
"""test host/smBase.py
"""
import libconf

from smBase import BaseHypervisor

bh = BaseHypervisor()
print bh.getLinuxNodeInfo()
print BaseHypervisor.getLinuxNodeInfo()
print BaseHypervisor.getLinuxCPUUsage()
#BaseHypervisor.linuxPowercycle()
