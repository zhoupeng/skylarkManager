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
    def ack_getMyAppList(username, passwd):
        """response to user's getmyapplist

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        """
        pass

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
    def ack_getAllAppList(username, passwd):
        """response to getallapplist

        @type username: str
        @param username: user name
        @type passwd: str
        @param passwd: password
        """
        pass

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
        ack = [CMDAccount.userunregister, {"status": status,
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
        req = [CMDAccount.userregister, {"username": username,
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
        @type orderlist: str
        @param orderlist: Order list
        """
        pass

    @staticmethod
    def ack_order(status, msg):
        """response to order request
        @type status: str
        @param status: auth success or fail("success", "fail")
        @type msg: str
        @param msg: message for detail
        """
        ack = [CMDAccount.ORDER, {"status": status,
                                      "msg": msg}]

        return json.dumps(ack)

