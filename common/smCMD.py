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
    # resource report, host <-(fetch)---(report)-> agent
    rsreport = "RSREPORT"
    # instance requrest, agent <-(ack)---(req)-> host
    reqinstance = "REQINSTANCE"

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

    @staticmethod
    def cmd_reqinstance(uuid, **reqparas):
        """ request to create a instance.
        agent -> host

        @type uuid: str
        @param uuid: the uuid of the host
        @type req: dict{type}
        @param req: request params
        """
        reqparas.update(uuid = uuid)
        r = [CMDHostAgent.reqinstance, reqparas]

        return json.dumps(r)

    @staticmethod
    def ack_reqinstance(uuid, **instance):
        """ request to create a instance.
        host -> agent

        @type uuid: str
        @param uuid: the uuid of the host
        @type instance: dict{type, spicehost, spiceport}
        @param instance: instance's appearance to client
        """
        instance.update(uuid = uuid)
        ack = [CMDHostAgent.reqinstance, instance]

        return json.dumps(ack)

class CMDClientAgent:
    # instance requrest, client (req)-> agent
    reqinstance = "REQINSTANCE"

    @staticmethod
    def cmd_reqinstance(type):
        """ request to create a instance
        client -> agent

        @type type: str
        @param type: the type of instance (e.g. winxp, word)
        """
        req = [CMDClientAgent.reqinstance, {'type': type}]
        
        return json.dumps(req)
    @staticmethod
    def ack_reqinstance(type, spicehost, spiceport):
        """ response to client
        agent -> client

        @type type: str
        @param type: the type of instance (e.g. winxp, word)
        @type spicehost: str
        @param spicehost: the listen ip addr of spice server
        @type spiceport: int
        @param spiceport: the listen port of spice server
        """
        req = [CMDClientAgent.reqinstance, {'type': type,
                                            'spicehost': spicehost,
                                            'spiceport': spiceport}]
        
        return json.dumps(req)

