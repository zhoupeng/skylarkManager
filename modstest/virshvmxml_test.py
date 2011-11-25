#!/usr/bin/env python
#
# Filename: modstest/virshvmxml_test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
import libconf
from smVirshXML import *

xml = 'testvm.xml'
vvmxml = VirshVMXML()
vvmxml.init(xml)

options = { VirshOptions.SPICEHOST: '192.168.1.187',
            VirshOptions.SPICEPORT: '6111'
          }
print vvmxml.adjust(**options)
