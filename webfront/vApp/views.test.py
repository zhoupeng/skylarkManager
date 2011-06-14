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

@csrf_exempt
def vAppReq(request):
    """ Deal with all the reqs(new instance, shutdown instance, save instance)
    from the clients, the req will be handled to the agent. 
    That is the django acts as reqs router.
    """
    
    ret = None
    body = request.read()
    print body
    print "CLIENTSRV_PORT %s" % CLIENTSRV_PORT
    jsobj = json.loads(body)
    req = jsobj[0]

    if req == CMDClientAgent.reqinstance:
        type = jsobj[1]['type']
        reqins = CMDClientAgent.cmd_reqinstance(type)
        soc = socket.socket(type = socket.SOCK_DGRAM)
        soc.sendto(reqins, ('192.168.1.187', CLIENTSRV_PORT))

        # None VM Instance
        ret = CMDClientAgent.ack_reqinstance(type, None, 0)

        ack_reqins = soc.recv(512)
        if ack_reqins:
            ret = ack_reqins

    return HttpResponse(ret, mimetype = 'application/json')

    ##############################################
    ##############################################
    """
    # just for test
    jsobj = CMDClientAgent.ack_reqinstance('winxp', '192.168.1.187', 6000)
    #return HttpResponse(jsobj, mimetype = 'application/json')
    #return HttpResponse("%s" % request)
    return HttpResponse("%s\n\n%s" % (request.read(), request))
    """


    ##############################################
    ##############################################
    """ Temp test for POST
    """
    """
    cmd = request.POST['CMD']
    type = request.POST['TYPE']
    reqins = CMDClientAgent.cmd_reqinstance(type)
    soc = socket.socket(type = socket.SOCK_DGRAM)
    soc.sendto(reqins, ('192.168.1.187', CLIENTSRV_PORT))

    ret = CMDClientAgent.ack_reqinstance(type, None, 0)

    ack_reqins = soc.recv(512)
    if ack_reqins:
        ret = ack_reqins

    return HttpResponse(ret, mimetype = 'application/json')
    """
