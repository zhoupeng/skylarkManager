#!/usr/bin/env python
#
# Filename: webfront/accounts/WSAccount.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
#
# Description:
# Simple response to some request.
# -------------------------------------------------------------------
from django.utils import simplejson as json

class CMDAccount:
    """Web Service definition for account.
    The WS call, parameter and response are defined in JSON format.
    """
    # commands
    userlogin = "USERLOGIN"
    userlogout = "USERLOGOUT"
    myapplist = "MYAPPLIST"
    allapplist = "APPLIST"
    userregister = "USERREGISTER"
    userunregister = "USERUNREGISTER"
    generalresp = "GENERALRESP"
    order = "ORDER"
    appinfo = "APPINFO"


    @staticmethod
    def api_login(username, passwd):
        """user login, used by test.

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        """
        req = [CMDAccount.userlogin, {'username': username,
                                      'passwd': passwd}]

        return json.dumps(req)

    @staticmethod
    def ack_login(status, msg):
        """response to user login request

        @type status: str
        @param status: auth success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: message for detail
        """
        ack = [CMDAccount.userlogin, {"status": status,
                                      "msg": msg}]

        return json.dumps(ack)

    @staticmethod
    def api_logout(username, passwd):
        """user logout, used by test.

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        """
        req = [CMDAccount.userlogout, {'username': username,
                                       'passwd': passwd}]

        return json.dumps(req)

    @staticmethod
    def ack_logout(status, msg):
        """response to user logout request

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: message for detail
        """
        ack = [CMDAccount.userlogout, {"status": status,
                                       "msg": msg}]

        return json.dumps(ack)

    @staticmethod
    def api_getMyAppList(username, passwd):
        """Get all the apps this user has applied

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        """
        req = [CMDAccount.myapplist, {"username": username,
                                      "passwd": passwd}]
        return json.dumps(req)

    @staticmethod
    def ack_getMyAppList(username, status, msg, apps = []):
        """response to user's get myapplist

        @type username: str
        @param username: user name
        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: message for detail
        @type apps: python list, like 
                    [{'type':xx, 'num': xx, 'state': xx}, {}]
        
        @return type: json str, the parameter part is like this
                      [{'instanceid': xx, 'type': xx, 'state': xx}]
                      instanceid is instance's name
        """
        tmpApps = []
        for i in apps:
            it = {'instanceid': '%s%s%s' % (username, i['type'], i['num']),
                  'type': i['type'],
                  'state': i['state']}
            tmpApps.append(it)

        ack = [CMDAccount.myapplist, {"status": status,
                                      "msg": msg,
                                      "apps": tmpApps}]

        return json.dumps(ack)

    @staticmethod
    def api_getAllAppList(username, passwd):
        """Get the app list published

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        """
        req = [CMDAccount.allapplist, {"username": username,
                                       "passwd": passwd}]
        return json.dumps(req)

    @staticmethod
    def ack_getAllAppList(status, msg, apps = []):
        """response to get allapplist

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: message for detail
        @type apps: python list, like 
                    [{'type':xx, 'logo': xx, 'description': xx}, {}]
        """
        ack = [CMDAccount.allapplist, {"status": status,
                                       "msg": msg,
                                       "apps": apps}]

        return json.dumps(ack)

    @staticmethod
    def api_getAppInfo(username, passwd, instanceid):
        """Get the information of user's specified app

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type instanceid: str
        @param instanceid: the name of instance
        """
        req = [CMDAccount.appinfo, {"username": username,
                                    "passwd": passwd,
                                    "instanceid": instanceid}]

        return json.dumps(req)

    @staticmethod
    def ack_getAppInfo(status, msg, info = {}):
        """response to get app info

        @type status: str
        @param status: success or fail(SUCCESS, FAIL)
        @type msg: str
        @param msg: message for detail
        @type info: python map, like 
          {'type':xx, 'logo': xx, 'description': xx, 'state': xx}
        """
        # TODO. Get more info about an instance, such as disk and vcpu

        ack = [CMDAccount.appinfo, {"status": status,
                                    "msg": msg,
                                    "info": info}]

        return json.dumps(ack)

    @staticmethod
    def api_register(username, passwd):
        """register as a valid user,
        More info need to be extended.

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        """
        # TODO. Email verifying support

        req = [CMDAccount.userregister, {"username": username,
                                         "passwd": passwd}]
        return json.dupms(req)

    @staticmethod
    def ack_register(status, msg):
        """response to user register request

        @type status: str
        @param status: auth success or fail("success", "fail")
        @type msg: str
        @param msg: message for detail
        """
        ack = [CMDAccount.userregister, {"status": status,
                                      "msg": msg}]

        return json.dumps(ack)

    @staticmethod
    def api_unRegister(username, passwd):
        """request to unregister from the system,

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        """
        req = [CMDAccount.userunregister, {"username": username,
                                           "passwd": passwd}]
        return json.dupms(req)

    @staticmethod
    def ack_unRegister(status, msg):
        """response to user unregister request

        @type status: str
        @param status: auth success or fail("success", "fail")
        @type msg: str
        @param msg: message for detail
        """
        ack = [CMDAccount.userunregister, {"status": status,
                                      "msg": msg}]

        return json.dumps(ack)

    @staticmethod
    def ack_generalResp(status, msg):
        """response to any request, just tell if success

        @type status: str
        @param status: auth success or fail("success", "fail")
        @type msg: str
        @param msg: message for detail
        """
        ack = [CMDAccount.generalresp, {"status": status,
                                        "msg": msg}]
        return json.dumps(ack)                                        

    @staticmethod
    def api_order(username, passwd, orderlist):
        """User request an order,
        if successful, user will get the permission accordingly. 

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        @type orderlist: list (that is [])
        @param orderlist: contain a list of service type to order
        """
        req = [CMDAccount.order, {'orderlist': orderlist}]
        return json.dumps(req)

    @staticmethod
    def ack_order(status, msg):
        """response to order request
        @type status: str
        @param status: auth success or fail("success", "fail")
        @type msg: str
        @param msg: message for detail
        """
        ack = [CMDAccount.order, {"status": status,
                                      "msg": msg}]

        return json.dumps(ack)

