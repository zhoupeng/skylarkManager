#!/usr/bin/env python
#
# Filename: modstest/xencheckpoint_test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
import libconf
from smCheckpoint import *

#ckpfile = '/home/zp/Desktop/fc8/hvm-WinXP/fedora14.ckp'
ckpfile = '/home/zp/Desktop/fc8/hvm-WinXP/fedora14.2048'
xckp = XenCheckpoint()
xckp.init(ckpfile)

print "%s" % xckp.geth_prefix()
#print "%i" % xckp.geth_size()
print "%d" % xckp.geth_size_val()
print "%s" % xckp.geth_head_cfg()

options = {XenOptions.SPICEHOST: '127.0.0.1',
           XenOptions.SPICEPORT: str(6666)}

xckp.adjustCKPHead(**options)
print "after adjustCKPHead()"
print "%s" % xckp.geth_prefix()
#print "%i" % xckp.geth_size()
print "%d" % xckp.geth_size_val()
print "%s" % xckp.geth_head_cfg()
print "%s" % xckp.getheader()
