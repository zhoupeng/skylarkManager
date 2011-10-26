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

class CMDClientAgent:
    # instance requrest, client (req)-> agent
    createinstance = "CREATEINSTANCE"
    releaseinstance = "RELEASEINSTANCE"
    saveinstance = "SAVEINSTANCE"
    restoreinstance = "RESTOREINSTANCE"
    startinstance = "STARTINSTANCE"
    shutdowninstance = "SHUTDOWNINSTANCE"
    getinstanceinfo = "GETINSTANCEINFO"
    newinstancebysnapshot = "NEWINSTANCEBYSNAPSHOT"

    @staticmethod
    def cmd_createInstance(owner, type, nth = "0"):
        """Request to create an instance
        webfront client -> agent
        You don't need to take care of the meaning of
        owner, type and nth in fact, they are used to
        define the vm/instance's name(instanceid).

        @type owner: str
        @param owner: the owner of vm
        @type type: str
        @param type: the type of instance (e.g. winxp, word)
        @type nth: str
        @param nth: how many now?
        """
        req = [CMDClientAgent.createinstance, {'owner': owner,
                                               'type': type,
                                               'nth': nth}]
        return json.dumps(req)

    @staticmethod
    def ack_createInstance(status, msg, instanceid, spicehost, spiceport):
        """ Response to webfront client
       
        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: describe the status in detail
        @type instanceid: str
        @param instanceid: the name of instance(ownertypenth),
        it's only necessary to keep this name unique, we don't need to transfer
        info from the instanceid(vm name)
        @type spicehost: str
        @param spicehost: the listen ip addr of spice server
        @type spiceport: int
        @param spiceport: the listen port of spice server
        """
        ack = [CMDClientAgent.createinstance, {'status': status,
                                               'msg': msg,
                                               'instanceid': instanceid,
                                               'spicehost': spicehost,
                                               'spiceport': spiceport}]
        
        return json.dumps(ack)

    @staticmethod
    def cmd_newInstanceBySnapshot(owner, type, nth = "0"):
        """The webfront Request to create an new instance from type
        snapshot(eg. xen checkpoint)
        It's different from restoreinstance cmd that the later
        restore an instance from it's own checkpoint file, while the former will
        create it's own checkpoint file from type snapshot.
        webfront client -> agent
        You don't need to take care of the meaning of
        owner, type and nth in fact, they are used to
        define the vm/instance's name(instanceid).

        @type owner: str
        @param owner: the owner of vm
        @type type: str
        @param type: the type of instance (e.g. winxp, word)
        @type nth: str
        @param nth: how many now?
        """
        req = [CMDClientAgent.newinstancebysnapshot, {'owner': owner,
                                                      'type': type,
                                                      'nth': nth}]
        return json.dumps(req)

    @staticmethod
    def ack_newInstanceBySnapshot(status, msg, hostuuid, instanceid,
                                  spicehost, spiceport):
        """ Response to webfront client
       
        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: describe the status in detail
        @type hostuuid: str
        @param hostuuid: the host running this instance
        @type instanceid: str
        @param instanceid: the name of instance(ownertypenth),
        it's only necessary to keep this name unique, we don't need to transfer
        info by the instanceid(vm name)
        @type spicehost: str
        @param spicehost: the listen ip addr of spice server
        @type spiceport: int
        @param spiceport: the listen port of spice server
        """
        ack = [CMDClientAgent.newinstancebysnapshot,
               {'status': status,
                'msg': msg,
                'hostuuid': hostuuid,
                'instanceid': instanceid,
                'spicehost': spicehost,
                'spiceport': spiceport}]
        
        return json.dumps(ack)

    @staticmethod
    def cmd_shutdownInstance(owner, type, nth, hostuuid):
        """
        @type owner: str
        @param owner: the owner of vm
        @type type: str
        @param type: the type of instance (e.g. winxp, word)
        @type nth: str
        @param nth: which one?
        @type hostuuid: str
        @param hostuuid: uuid of node hosting this instance
        """
        req = [CMDClientAgent.shutdowninstance, {'owner': owner,
                                                 'type': type,
                                                 'nth': nth,
                                                 'hostuuid': hostuuid}]
        return json.dumps(req)

    @staticmethod
    def ack_shutdownInstance(status, msg):
        """ Response to webfront client

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: describe the status in detail
        """
        ack = [CMDClientAgent.shutdowninstance, {'status': status,
                                                 'msg': msg}]
        return json.dumps(ack)

    @staticmethod
    def cmd_restoreInstance(owner, type, nth, hostuuid):
        """
        @type owner: str
        @param owner: the owner of vm
        @type type: str
        @param type: the type of instance (e.g. winxp, word)
        @type nth: str
        @param nth: which one?
        @type hostuuid: str
        @param hostuuid: uuid of node hosting this instance
        """
        req = [CMDClientAgent.restoreinstance, {'owner': owner,
                                                'type': type,
                                                'nth': nth,
                                                'hostuuid': hostuuid}]
        return json.dumps(req)

    @staticmethod
    def ack_restoreInstance(status, msg, instanceid, spicehost, spiceport):
        """ Response to webfront client

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: describe the status in detail
        @type instanceid: str
        @param instanceid: the name of instance(ownertypenth),
        it's only necessary to keep this name unique,
        we don't need to transfer info from the instanceid(vm name)
        @type spicehost: str
        @param spicehost: the listen ip addr of spice server
        @type spiceport: int
        @param spiceport: the listen port of spice server
        """
        ack = [CMDClientAgent.restoreinstance, {'status': status,
                                               'msg': msg,
                                               'instanceid': instanceid,
                                               'spicehost': spicehost,
                                               'spiceport': spiceport}]
        return json.dumps(ack)

class CMDHostAgent:
    # host join, host <-(ack)---(req)-> agent
    join = "HOSTJOIN"
    # resource report, host <-(fetch)---(report)-> agent
    rsreport = "RSREPORT"
    # instance creating, agent <-(ack)---(req)-> host
    createinstance = CMDClientAgent.createinstance
    # instance creating from snapshot(Xen checkpoint file)
    # agent <-(ack)---(req)-> host
    newinstancebysnapshot = CMDClientAgent.newinstancebysnapshot
    # shutdown the instance, delete the snapshot (if exist) but keep the image
    # agent <-(ack)---(req)-> host
    shutdowninstance = CMDClientAgent.shutdowninstance
    # restore the instance
    # agent <-(ack)---(req)-> host
    restoreinstance = CMDClientAgent.restoreinstance

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
    def cmd_createInstance(uuid, owner, type, nth):
        """ request to create an instance.
        agent -> host

        In fact, we use 'owner type nth' to construct the 
        unique name for an instance,
        we don't take care user info except in webfront.

        @type uuid: str
        @param uuid: the uuid of the host
        @type owner: str
        @param owner: the owner of this instance
        @type type: str
        @params type: the type of this instance(winxp, word ...)
        @type nth: str
        @params nth: how many now (0, 1, ...)
        """
        r = [CMDHostAgent.createinstance, {'uuid': uuid,
                                           'owner': owner,
                                           'type': type,
                                           'nth': nth}]

        return json.dumps(r)


    @staticmethod
    def ack_createInstance(uuid, **instance):
        """ ack to request to create an instance.
        host -> agent

        @type uuid: str
        @param uuid: the uuid of the host
        @type instance: dict{status, msg, owner, type, nth, spicehost, spiceport}
        @param instance: instance's appearance to client
        """
        instance.update(uuid = uuid)
        ack = [CMDHostAgent.createinstance, instance]

        return json.dumps(ack)

    @staticmethod
    def cmd_newInstanceBySnapshot(uuid, owner, type, nth):
        """ request to create an instance from snapshot file
        agent -> host

        In fact, we use 'owner type nth' to construct the 
        unique name for an instance,
        we don't take care user info except in webfront.

        @type uuid: str
        @param uuid: the uuid of the host
        @type owner: str
        @param owner: the owner of this instance
        @type type: str
        @params type: the type of this instance(winxp, word ...)
        @type nth: str
        @params nth: how many now (0, 1, ...)
        """
        r = [CMDHostAgent.newinstancebysnapshot,
             {'uuid': uuid,
              'owner': owner,
              'type': type,
              'nth': nth}]

        return json.dumps(r)

    @staticmethod
    def ack_newInstanceBySnapshot(uuid, **instance):
        """ ack to request to create an instance by snapshot.
        host -> agent

        @type uuid: str
        @param uuid: the uuid of the host
        @type instance: dict{status, msg, owner, type, nth, spicehost, spiceport}
        @param instance: instance's appearance to client
        """
        instance.update(uuid = uuid)
        ack = [CMDHostAgent.newinstancebysnapshot, instance]

        return json.dumps(ack)

    @staticmethod
    def cmd_shutdownInstance(uuid, owner, type, nth):
        """ request to shutdown an instance
        agent -> host

        In fact, we use 'owner type nth' to find the 
        unique name for an instance,
        we don't take care user info except in webfront.

        @type uuid: str
        @param uuid: the uuid of the host
        @type owner: str
        @param owner: the owner of this instance
        @type type: str
        @params type: the type of this instance(winxp, word ...)
        @type nth: str
        @params nth: how many now (0, 1, ...)
        """
        r = [CMDHostAgent.shutdowninstance,
             {'uuid': uuid,
              'owner': owner,
              'type': type,
              'nth': nth}]

        return json.dumps(r)

    @staticmethod
    def ack_shutdownInstance(uuid, status, msg, owner, type, nth):
        """ ack to request to shutdown an instance.
        host -> agent

        @type uuid: str
        @param uuid: the uuid of the host
        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: describe the status in detail
        @type owner: str
        @param owner: the owner of this instance
        @type type: str
        @params type: the type of this instance(winxp, word ...)
        @type nth: str
        @params nth: which one?
        """
        ack = [CMDHostAgent.shutdowninstance, {"uuid": uuid,
                                               "status": status,
                                               "msg": msg,
                                               "owner": owner,
                                               "type": type,
                                               "nth": nth}]

        return json.dumps(ack)

    @staticmethod
    def cmd_restoreInstance(uuid, owner, type, nth):
        """ request to restore the instance from it's snapshot file
        agent -> host

        In fact, we use 'owner type nth' to construct the 
        unique name for an instance,
        we don't take care user info except in webfront.

        @type uuid: str
        @param uuid: the uuid of the host,
        let the host to check if this req is to itself
        @type owner: str
        @param owner: the owner of this instance
        @type type: str
        @params type: the type of this instance(winxp, word ...)
        @type nth: str
        @params nth: how many now (0, 1, ...)
        """
        r = [CMDHostAgent.restoreinstance,
             {'uuid': uuid,
              'owner': owner,
              'type': type,
              'nth': nth}]

        return json.dumps(r)

    @staticmethod
    def ack_restoreInstance(uuid, **instance):
        """ ack to request to restore itself from it's snapshot.
        host -> agent

        @type uuid: str
        @param uuid: the uuid of the host
        @type instance: dict{status, msg, owner, type, nth, spicehost, spiceport}
        @param instance: instance's appearance to client
        """
        instance.update(uuid = uuid)
        ack = [CMDHostAgent.restoreinstance, instance]

        return json.dumps(ack)
