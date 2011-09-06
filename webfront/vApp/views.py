#!/usr/bin/env python
#
# Filename: webfront/vApp/views.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
#
# -------------------------------------------------------------------
""" This module include the main logic to deal with vApp reqs from the clients.
It's the most front end, acting as reqs messenger between the clients and the agent. 

It mainly has two aspects of work:
    1) Authenticate the coming req.
    2) messeager between client and agent.

    that is:
    check to authenticate the validity of coming req.
    if valid, then
        handle the req to the agent
        waiting for dealing result from the agent
        send the result to the client as respond
    else
        tell the client the req is invalid.
"""
import libconf

from django.http import HttpResponse
from django.utils import simplejson as json
from smCMD import *
import socket
from smSettings import *

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from webfront.accounts.WSAccount import CMDAccount

from django.contrib import auth

from smTypes import *
from WSvApp import *
from webfront.accounts.models import *

@csrf_exempt
def api_vapp(request):
    """ Deal with all the reqs(new instance, shutdown instance, save instance)
    from the clients, the req will be handled to the agent. 
    That is the django acts as reqs router.
    """
    if not request.user.is_authenticated():
        # Limiting these access to logged-in users
        jsstr = CMDAccount.ack_generalResp(Status.FAIL, "login first")
        return HttpResponse(jsstr, mimetype = 'application/json')

    # get data from different format ...
    body = request.read()
     
    # translate different format to jsobj ...
    data = body
    print body
    print "CLIENTSRV_PORT %s" % CLIENTSRV_PORT
    jsobj = json.loads(data)
    # TODO. Error checking
    cmd = jsobj[0]
    uname = jsobj[1]['username']
    passwd = jsobj[1]['passwd']

    if cmd not in [CMDvApp.reqinstance, CMDvApp.createimage,
                   CMDvApp.createinstance, CMDvApp.newinstancebysnapshot,
                   CMDvApp.releaseinstance, CMDvApp.startinstance,
                   CMDvApp.shutdowninstance, CMDvApp.saveinstance,
                   CMDvApp.restoreinstance, CMDvApp.getinstanceinfo]:
        jsstr = CMDAccount.ack_generalResp(Status.FAIL, "Invalid WebAPI")
        return HttpResponse(jsstr, mimetype = 'application/json')

    if cmd == CMDvApp.reqinstance:
        jsstr = reqInstance(uname, passwd, type)
        return HttpResponse(ret, mimetype = 'application/json')
    elif cmd == CMDvApp.newinstancebysnapshot:
        type = jsobj[1]['type']
        jsstr = newInstanceBySnapshot(uname, passwd, type)
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDvApp.shutdowninstance:
        instanceid = jsobj[1]['instanceid']
        jsstr = shutdownInstance(uname, passwd, instanceid)
        return HttpResponse(jsstr, mimetype = 'application/json')

def reqInstance(username, passwd, type):
    """request an instance, it will create one when username haven't
    instance of type and otherwise return an existing instance.

    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type type: str
    @param type: the type of the instance
    """
    pass

def createInstance(username, passwd, type):
    """Create an instance from scratch.
    Assume the disk img is there.

    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type type: str
    @param type: the type of the instance
    """
    user = auth.authenticate(username = username, password = passwd)
    if not user:
        return CMDvApp.ack_createInstance(Status.FAIL,
                                          'invalid username or passord')
    od_qs = Order.objects.filter(user = user)
    od = None
    for i in od_qs:
        if i.service.type == type and i.state == OrderState.ordered:
            od = i
            break
    if od:
        crtIns = CMDClientAgent.cmd_createInstance(username,
                                                   type, "%s" % od.num)
        soc = socket.socket(type = socket.SOCK_DGRAM)
        soc.sendto(crtIns, (CLIENTSRV_HOST, CLIENTSRV_PORT))

        ackCrtIns = soc.recv(1024)
        soc.close()

        if not ackCrtIns:
            return CMDvApp.ack_createInstance(Status.FAIL,
                                              'internal err')
        jsobj = json.loads(ackCrtIns)
        # In fact, the instanceid is the same between agent and webfront,
        # It's part of jsobj[1]['instanceid'], but it's different from the
        # real instance name because our storage system need special name format
        # to get info. Because it's transparent.
        instanceid = "%s%s%s" % (username, od.service.type, od.num)
        spicehost = jsobj[1]['spicehost']
        spiceport = jsobj[1]['spiceport']
        info = {'instanceid': instanceid,
                'spicehost': spicehost, 'spiceport': spiceport}
        return CMDvApp.ack_createInstance(jsobj[1]['status'],
                                          jsobj[1]['msg'], info)
    else:
        return CMDvApp.ack_createInstance(Status.FAIL,
                                          'there is no free order for you')


def releaseInstance(username, passwd, instanceid):
    """Release all resource of instanceid (destroy instanceid)
    
    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type instanceid: str
    @param instanceid: the id of the instance
    """
    pass

def startInsance(username, passwd, instanceid):
    """start an existing instance
    
    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type instanceid: str
    @param instanceid: the id of the instance
    """
    pass

def shutdownInstance(username, passwd, instanceid):
    """shutdown an instance (OrderState.STOPED)
    
    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type instanceid: str
    @param instanceid: the id of the instance
    """
    user = auth.authenticate(username = username, password = passwd)
    if not user:
        return CMDvApp.ack_shutdownInstance(Status.FAIL,
                                            'invalid username or passord')

    od_qs = Order.objects.filter(user = user)
    od = None
    for i in od_qs:
        if instanceid == i.instanceID():
            od = i 
            break

    if not od:
        return CMDvApp.ack_shutdownInstance(Status.FAIL,
                               "the instance %s doesn't exist" % instanceid)
    shutdownins = CMDClientAgent.cmd_shutdownInstance(username,
                                                      od.service.type,
                                                      "%s" % od.num)
    soc = socket.socket(type = socket.SOCK_DGRAM)
    soc.sendto(shutdownins, (CLIENTSRV_HOST, CLIENTSRV_PORT))

    ackShutDown = soc.recv(128)
    if not ackShutDown:
        return CMDvApp.ack_shutdownInstance(Status.FAIL,
                                            'internal err')
    jsobj = json.loads(ackShutDown)
    
    if jsobj[1]['status'] == Status.FAIL:
        return CMDvApp.ack_shutdownInstance(jsobj[1]['status'],
                                            jsobj[1]['msg'])

    od.state = OrderState.STOPED
    od.save()

    return CMDvApp.ack_shutdownInstance(jsobj[1]['status'],
                                        jsobj[1]['msg'])

def saveInstance(username, passwd, instanceid):
    """Save the state of an instance then shutdown
    
    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type instanceid: str
    @param instanceid: the id of the instance
    """
    pass

def restoreInstance(username, passwd, instanceid):
    """restore an instance from the state saved before
    
    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type instanceid: str
    @param instanceid: the id of the instance
    """
    pass

def getInstanceInfo(username, passwd, instanceid):
    """get the detail info of an instance no matter running or stoped
    
    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type instanceid: str
    @param instanceid: the id of the instance
    """
    pass

def newInstanceBySnapshot(username, passwd, type):
    """Create an instance from snapshot

    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type type: str
    @param type: the type of the instance
    """
    user = auth.authenticate(username = username, password = passwd)
    if not user:
        return CMDvApp.ack_newInstanceBySnapshot(Status.FAIL,
                                                 'invalid username or password')
    
    od_qs = Order.objects.filter(user = user)
    od = None
    for i in od_qs:
        if i.service.type == type and i.state == OrderState.ORDERED:
            od = i
            break
    if od:
        newInsBySnap = CMDClientAgent.cmd_newInstanceBySnapshot(username,
                                                           type,
                                                           "%s" % od.num)
        soc = socket.socket(type = socket.SOCK_DGRAM)
        soc.sendto(newInsBySnap, (CLIENTSRV_HOST, CLIENTSRV_PORT))

        ackNewInsBySnap = soc.recv(1024)
        if not ackNewInsBySnap:
            return CMDvApp.ack_newInstanceBySnapshot(Status.FAIL,
                                                     'internal err')
        jsobj = json.loads(ackNewInsBySnap)
        instanceid = "%s%s%s" % (username, od.service.type, od.num)
        spicehost = jsobj[1]['spicehost']
        spiceport = jsobj[1]['spiceport']
        info = {'instanceid': instanceid,
                'spicehost': spicehost, 'spiceport': spiceport}

        od.state = OrderState.RUNNING
        od.save()

        return CMDvApp.ack_newInstanceBySnapshot(jsobj[1]['status'],
                                                 jsobj[1]['msg'], info)
    else:
        return CMDvApp.ack_newInstanceBySnapshot(Status.FAIL,
                                          'there is no free order for you')

