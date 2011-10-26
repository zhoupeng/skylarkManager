#!/usr/bin/env python
#
# Filename: host/smHostMain.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------

import libconf
import smHost 
from CONSTANTS import *

if __name__ == '__main__':
    host = smHost.Host(MASTER_AGENT_HOST, MASTER_AGENT_PORT)

    print "Try to join in the cluster ..."
    if (not host.joinIn()):
        print "Fail to joinin the cluster!"
        sys.exit(0)
    print "Succeed to joinin the cluster!"

    host.start()
