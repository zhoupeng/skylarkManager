#!/usr/bin/env python
#
# Filename: host/smMain.py
#
# -------------------------------------------------------------------
#
# 
#
# -------------------------------------------------------------------

import smXen 
import simplejson as json

node = smXen.XenNode()

if __name__ == '__main__':

    meminfo = node.getMemInfo();
    for key in meminfo:
        print '%s:%s' %(key, meminfo[key])

