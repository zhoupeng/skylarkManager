#!/usr/bin/env python
#
# Filename: host/test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------
import libconf

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

    # smXen 
    import smXen 
    xennode = smXen.XenNode()

    #print smXen.XenNode._getXMList(include_node = True)
    print xennode.getNodeInfo();
    #print xennode.verify()

    #print smXen.XenNode._getXentop()
    print xennode.getCPUUsage()

    # smNet
    import smNet
    hostname1 = smNet.getHostname()
    print hostname1.name
    print hostname1.ip

    hostname2 = smNet.getHostname('cloud-os.org')
    print hostname2.name
    print hostname2.ip
    
    print smNet.Hostname.getSysName()
    print smNet.Hostname.getFqdn('nfs.iscas.ac.cn')

    print smNet.tcpPing(hostname2.ip, 80)
    print smNet.tcpPing(hostname2.ip, 8080)

    #IPV4 127.0.0.0 to 127.255.255.255
    #IPV6 0:0:0:0:0:0:0:1 (also written as ::1)
    print smNet.IP4Address.isLoopback('127.255.255.255')
    print smNet.IP6Address.isLoopback('::1')
    print smNet.IP4Address.isLoopback('128.0.0.1')

    # smHost
    import smHost
    h1 = smHost.Host("192.168.1.187", 1234)
    #h1 = smHost.Host("192.168.1.187", -1)
    print h1.join()

