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
    # host join, host <-(ack)---(req)-> agent
    join = "HOSTJOIN"
    # resource report host <-(fetch)---(report)-> agent
    rsreport = "RSREPORT"

    @staticmethod
    def cmd_join(uuid, **hostmisc):
        """host join request
        
        @type uuid: str
        @param uuid: the host's identifier, global unique.
        @type hostmisc
        @type type: the type of host(xen, kvm ...), currently only xen supported
        """
        # dict.update return None
        hostmisc.update(uuid = uuid)
        req = [CMDHostAgent.join, hostmisc]
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

    @staticmethod
    def cmd_rsreport(uuid, **rs):
        """ resource report to agent periodically

        @type uuid: str
        @param uuid: the uuid of the host
        @type rs: dict{cpurate, total_memory, free_memory, memory_dom0}
        @param rs: resource report content
        """
        rs.update(uuid = uuid)
        rep = [CMDHostAgent.rsreport, rs]

        return json.dumps(rep)

    @staticmethod
    def fetch_RSReport(uuid):
        """ agent fetch resource report acctively,
        reserved, it will almost never be used.

        @type uuid: str
        @param uuid: the uuid of the host
        """
        fetch = [CMDHostAgent.rsreport, {'uuid': uuid}]

        return json.dumps(fetch)
