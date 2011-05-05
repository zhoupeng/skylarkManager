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
import sys
import simplejson as json
class Test: 
    def _GetOutput(self):
        """Returns the combined stdout and stderr for easier usage.
    
        """
        #return sys.stdout + sys.stderr
        return "property test.", self.output 

    output = property(_GetOutput, None, None, "Return full output")


if __name__ == '__main__':

    #test = Test()
    #print (test._GetOutput())
    xennode = smXen.XenNode()

    #print smXen.XenNode._getXMList(include_node = True)
    print xennode.getNodeInfo();
    #print xennode.verify()

    #print smXen.XenNode._getXentop()
    print xennode.getCPUUsage()

