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
#print kvm.getNodeInfo()
#print kvm.generateKVMRuntime('testvm', '192.168.1.187', '6200', 350)
#print kvm.createInstance1('testvm', '192.168.1.187', '6200', 350)
#print kvm.createInstance('testvm', '192.168.12.236', 6200, 350)
#print kvm.shutdownInstance('testvm')
#print KVMNode._runVirshDumpxml('testvm')
print kvm.saveInstance('testvm')
#print kvm.newInstanceBySnapshot('testvm', '192.168.12.236', 6200)
kvm.restoreInstance('testvm', '192.168.12.236', 6201)
