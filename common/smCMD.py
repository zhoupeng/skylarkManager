#!/usr/bin/env python
#
# Filename: common/smCMD.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
# 
# -------------------------------------------------------------------
import simplejson as json

class CMDHostAgent:
    join = "HOSTJOIN"
    
    @staticmethod
    def cmd_join(uuid, type):
        """host join request
        
        @type uuid: str
        @param uuid: the host's identifier, global unique.
        @type type: the type of host(xen, kvm ...), currently only xen supported
        """
        req = [CMDHostAgent.join, {'uuid': uuid,
                                   'type': type}]
        return json.dumps(req)

    @staticmethod
    def ack_join(uuid, succeed):
        """ ACK to host join req

        @type uuid: str
        @param uuid: the uuid of the host
        @type succeed: bool
        @param succeed: True-successful, False-unsuccessful
        """
        ack = [CMDHostAgent.join, {'uuid': uuid,
                                   'succeed': succeed}]
        return json.dumps(ack)

