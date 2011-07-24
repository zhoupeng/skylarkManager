#!/usr/bin/env python
#
# Filename: webfront/accounts/WSvApp.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.07 ~
#
# Description:
# vApp function API requests.
# This file defined the outher web api
# -------------------------------------------------------------------
from django.utils import simplejson as json

class CMDvApp:
    """Web Service definition for vApp.
    The WS call, parameter and response are defined in JSON format.
    The api_xx only describe the interface, which is not used by the
    system except the test utility.
    ack_xx describe the response format, which is used by the system
    to pack the WS return valude in JSON.

    Orginally it just re-use common/smCMD.CMDClientAgent to describe
    the web service API, but it will introduce some restriction,
    e.g. must keep one-to-one mapping between WS-API with CMDClientAgent,
    but WS-API is user-oriented and CMDClientAgent are basic functional
    commands(interface) used internally, one WS-API can correspond to
    one or multiple CMDClientAgent command.
    """

    # commands
    reqinstance = "REQINSTANCE"
    createimage = "CREATEIMAGE"
    createinstance = "CREATEINSTANCE"
    # Function necessary but I'm not sure if it's proper to be WS API
    # open to user.
    newinstancebysnapshot = "NEWINSTANCEBYSNAPSHOT" 
    releaseinstance = "RELEASEINSTANCE"
    startinstance = "STARTINSTANCE"
    shutdowninstance = "SHUTDOWNINSTANCE"
    saveinstance = "SAVEINSTANCE"
    restoreinstance = "RESTOREINSTANCE"
    getinstanceinfo = "GETINSTANCEINFO"

    @staticmethod
    def api_reqInstance(username, passwd, type):
        """request an instance, it will create one when username haven't
        instance of type and otherwise return an existing instance.

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type type: str
        @param type: the type of the instance
        """
        req = [CMDvApp.reqinstance, {'username': username,
                                     'passwd': passwd}]
        return json.dumps(req)


    @staticmethod
    def ack_reqInstance(status, msg, type, instanceid, spicehost, spiceport):
        """Response to reqinstance request

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type type: str
        @param type: the type of instance (e.g. winxp, word)
        @type instanceid: str
        @param instanceid: the unique identifier(instance name used in fact)
        @type spicehost: str
        @param spicehost: the listen ip addr of spice server
        @type spiceport: int
        @param spiceport: the listen port of spice server
        """

        ack = [CMDvApp.reqinstance, {'status': status,
                                     'msg': msg,
                                     'type': type,
                                     'instanceid':instanceid,
                                     'spicehost': spicehost,
                                     'spiceport': spiceport}]
        return ack

    @staticmethod
    def api_createImage(username, passwd, type):
        """Alloc necessary resource for an instance, without launching it.
        Reserved.
 
        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type type: str
        @param type: the type of the instance
        """
        req = [CMDvApp.createimage, {'username': username,
                                     'passwd': passwd,
                                     'type': type}]
        return json.dumps(req)

    @staticmethod
    def ack_createImage(status, msg, imageid):
        """Response to createImage request
        Reserved

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: detailed describtion
        @type imageid: str
        @param imageid: the id of the image
        """
        ack = [CMDvApp.createimage, {'status': status,
                                     'msg': msg
                                     'imageid': imageid}]
        return json.dumps(ack)

    @staticmethod
    def api_createInstance(username, passwd, type):
        """Create an instance.
        Assume the disk img is there.

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type type: str
        @param type: the type of the instance
        """
        req = [CMDvApp.createinstance, {'username': username,
                                        'passwd': passwd,
                                        'type': type}]
        return json.dumps(req)

    @staticmethod
    def ack_createInstance(status, msg, info = {}):
        """Response to createinstance request

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: detailed describtion
        @type info: python map, like
        {'instanceid':xx, 'spicehost': xx, 'spiceport': xx}
        @param info: the necessary infomation for
        client to access the instance.
            * type instanceid: str
            * param instanceid: the unique identifier
              (instance name used in fact)
            * type spicehost: str
            * param spicehost: the listen ip addr of spice server
            * type spiceport: int
            * param spiceport: the listen port of spice server

        """

        ack = [CMDvApp.createinstance, {'status': status,
                                        'msg': msg,
                                        'info': info}]
        return ack

    @staticmethod
    def api_newInstanceBySnapshot(username, passwd, type):
        """Create an instance from snapshot
 
        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type type: str
        @param type: the type of the instance
        """
        req = [CMDvApp.newinstancebysnapshot, {'username': username,
                                               'passwd': passwd,
                                               'type': type}]
        return json.dumps(req)

    @staticmethod
    def ack_newInstanceBySnapshot(status, msg, info = {}):
        """Response to newinstancebysnapshot request

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: detailed describtion
        @type info: python map, like
        {'instanceid':xx, 'spicehost': xx, 'spiceport': xx}
        @param info: the necessary infomation for
        client to access the instance.
            * type instanceid: str
            * param instanceid: the unique identifier
              (instance name used in fact)
            * type spicehost: str
            * param spicehost: the listen ip addr of spice server
            * type spiceport: int
            * param spiceport: the listen port of spice server
        """

        ack = [CMDvApp.newinstancebysnapshot, {'status': status,
                                               'msg': msg,
                                               'info': info}]
        return json.dumps(ack)

    @staticmethod
    def api_releaseInstance(username, passwd, instanceid):
        """Release all resource of instanceid (destroy instanceid)
        
        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type instanceid: str
        @param instanceid: the id of the instance
        """
        req = [CMDvApp.releaseinstance, {'username': username,
                                         'passwd': passwd,
                                         'instanceid': instanceid}]
        return json.dumps(req)

    @staticmethod
    def ack_releaseInstance(status, msg):
        """Response to releaseinstance request

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: detailed describtion
        """
        ack = [CMDvApp.releaseinstance, {'status': status,
                                         'msg': msg}]
        return json.dumps(ack)

    @staticmethod
    def api_startInsance(username, passwd, instanceid):
        """start an existing instance
        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type instanceid: str
        @param instanceid: the id of the instance(the instance's name in fact)
        """
        req = [CMDvApp.startinstance, {'username': username,
                                       'passwd': passwd,
                                       'instanceid': instanceid}]
        return json.dumps(req)

    @staticmethod
    def ack_startInsance(status, msg, instanceid = None,
                         spicehost = None, spiceport = 0):
        """Response to STARTINSTANCE request,
        if SUCCESS, the instanceid, spicehost and spiceport are valid,
        otherwise they are invalid. The instanceid keep the same with
        api_startInsance.

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: detailed describtion
        @type instanceid: str
        @param instanceid: the id of the instance(instance's name used in fact)
        """
        ack = [CMDvApp.startinstance, {'status': status,
                                       'msg': msg,
                                       'instanceid': instanceid,
                                       'spicehost': spicehost,
                                       'spiceport': spiceport}]
        return json.dumps(ack)

    @staticmethod
    def api_shutdownInstance(username, passwd, instanceid):
        """shutdown an instance
        
        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type instanceid: str
        @param instanceid: the id of the instance
        """
        req = [CMDvApp.shutdowninstance, {'username': username,
                                          'passwd': passwd,
                                          'instanceid': instanceid}]
        return json.dumps(req)

    @staticmethod
    def ack_shutdownInstance(status, msg):
        """Response to shutdowninstance request

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: detailed describtion
        """
        ack = [CMDvApp.shutdowninstance, {'status': status,
                                          'msg': msg}]
        return json.dumps(ack)

    @staticmethod
    def api_saveInstance(username, passwd, instanceid):
        """Save the state of an instance to restore later.

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type instanceid: str
        @param instanceid: the name of the instance
        """
        req = [CMDvApp.saveinstance, {'username': username,
                                      'passwd': passwd,
                                      'instanceid': instanceid}]
        return json.dumps(req)                                      

    @staticmethod
    def ack_saveInstance(status, msg):
        """Response to saveinstance request

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: detailed describtion
        """
        ack = [CMDvApp.saveinstance, {'status': status,
                                         'msg': msg}]
        return json.dumps(ack)


    @staticmethod
    def api_restoreInstance(username, passwd, instanceid):
        """ The instanceid(instance name) is used to find the checkpoint file,
        the restored instanceid can be different from the param instanceid, the
        restored instanceid is provided by the response.
        This api is used to restore an instance saved before by user,
        not for the system to create an instance from snapshot

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type instanceid: str
        @param instanceid: the name of the instance
        """
        req = [CMDvApp.restoreinstance, {'username': username,
                                         'passwd': passwd,
                                         'instanceid': instanceid}]
        return json.dumps(req)

    @staticmethod
    def ack_restoreInstance(status, msg, instanceid):
        """Response to restoreinstance request

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: detailed describtion
        @type instanceid: str
        @param instanceid: The name of the restored instance
        """
        ack = [CMDvApp.restoreinstance, {'status': status,
                                         'msg': msg,
                                         'instanceid': instanceid}]
        return json.dumps(ack)

    @staticmethod
    def api_getInstanceInfo(username, passwd, instanceid):
        """ Get the infomation of instanceid
        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type instanceid: str
        @param instanceid: the name of the instance
        """
        req = [CMDvApp.getinstanceinfo, {'username': username,
                                         'passwd': passwd,
                                         'instanceid': instanceid}]
        return json.dumps(req)

    @staticmethod
    def ack_getInstanceInfo(status, msg, info):
        """Response to getinstanceinfo request 
        """
        pass

