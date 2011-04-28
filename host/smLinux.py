#!/usr/bin/env python
#
# Filename: host/smLinux.py
#
# -------------------------------------------------------------------
#
# 
#
# -------------------------------------------------------------------

import smUtility

class LinuxNode(object):

    def getMemInfo(self):
        '''
        routine to get mem info as a directory
        specifically:
        input is a sequence of "Label:", "Value", "kB"
        output is a  directory of "Label" -> int(Value)
        Add two fields:
        "UserspaceFree": how much memory is available for userspace (discounted buffers+caches)
        "SwapUsed": how much of swap is currently in use
        '''
        ret = {}
  
        lines = smUtility.parseSplitFile("/proc/meminfo")
        for line in lines:
            # line is list
            label = line[0]
            # skip over line that starts with 'total:' (2.4 kernel has
            # it at the start and we can't parse that)
            if line[0] == 'total:':
                continue
            # only accept lines that have colons after labels
            if label.endswith(":"):
                ret[label[:-1]] = int(line[1])
      
        # add couple of our own fields
        ret["UserspaceFree"] = ret["MemFree"] + ret["Buffers"] + ret["Cached"]
        ret["SwapUsed"] = ret["SwapTotal"] - ret["SwapFree"]
    
        return ret 

    def getCPUInfo(self):
        pass
