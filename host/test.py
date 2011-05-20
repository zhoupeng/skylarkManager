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

    # json
    # http://docs.python.org/library/json.html
    import simplejson as json
    # Encoding
    pylist = ['foo', {'bar': ('baz', None, 1.0, 2)}]
    encoded = json.dumps(pylist, indent = 4)
    print encoded
    # Decoding
    jstr = '["foo", {"bar":["baz", null, 1.0, 2]}]'
    decoded = json.loads(jstr)
    print decoded[1]

    # smHost
    import smHost
    h1 = smHost.Host("192.168.1.187", 1234)
    #h1 = smHost.Host("192.168.1.187", -1)
    print h1.joinIn()
    h1.start()

