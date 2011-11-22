#!/usr/bin/env python
#
# Filename: modstest/kvmHypervisor_test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
"""test host/smKVM.py
"""
import libconf

from smKVM import KVMNode

kvm = KVMNode()
print kvm.getType()
print kvm.getCPUUsage()
print kvm.getNodeInfo()

