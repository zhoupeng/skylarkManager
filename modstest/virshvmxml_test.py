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
            VirshOptions.SPICEPORT: '6111',
            VirshOptions.AGENTMOUSE: 'server',
            VirshOptions.FSSOURCEDIR: '/etc/skylark/usprvdata/testprvstorage',
            VirshOptions.FSTARGETDIR: 'mynewdata',
            VirshOptions.FSDRTYPE: 'handle',
            VirshOptions.FSDRWRPOLOCY: 'default',
            VirshOptions.FSTYPE: 'file',
            VirshOptions.FSACCESSMODE: 'passthrough'
          }
print vvmxml.adjust(**options)
print vvmxml.find("devices/graphics")
print vvmxml.find("devices/notexist")
print vvmxml.append(vvmxml.find("devices/graphics"),
"<lev1 test='test'><lev21/><lev22/></lev1>")
