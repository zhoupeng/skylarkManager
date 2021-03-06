#!/usr/bin/env python
#
# Filename: webfront/accounts/account.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
#
# -------------------------------------------------------------------
import libconf

from django.utils import simplejson as json
from django.http import HttpResponse

from django.contrib import auth

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from WSAccount import *

from smTypes import *

from models import *

@csrf_exempt
def api_account(request):
    """The account related uniform entry.
    It is responsible for
     * Parameter parsing,
     * Parameter err checking,
     * Call routing,
     * Distinguish to deal with different request formats/clients
       (Get, Post, Body, Ajax, JSON, XML ...) to hide the detail
       from the underneath, which is the most important.
     * Distinguish to deal with different clients to give different response,
       e.g. for browser, redirect to login view,
       for app client just return a status in JSON.

    The CMDAccount.userlogin api is divorced from api_account because
    api_login is used as login_required decorator
    """
    # get data from different format ...
    body = request.read()
     
    print body # for debug     
    # translate different format to jsobj ...
    data = body
    jsobj = json.loads(data)
    # TODO. Error checking
    cmd = jsobj[0]
    uname = jsobj[1]['username']
    passwd = jsobj[1]['passwd']
    
    if cmd not in [CMDAccount.userlogin, CMDAccount.userlogout,
                   CMDAccount.myapplist, CMDAccount.allapplist,
                   CMDAccount.userregister, CMDAccount.userunregister,
                   CMDAccount.order, CMDAccount.appinfo,
                   CMDAccount.unorder]:
        jsstr = CMDAccount.ack_generalResp(Status.FAIL, "Invalid WebAPI")
        return HttpResponse(jsstr, mimetype = 'application/json')

    if cmd not in [CMDAccount.userregister, CMDAccount.userlogin]:
        if not request.user.is_authenticated():
            # Limiting these access to logged-in users
            jsstr = CMDAccount.ack_generalResp(Status.FAIL, "login first")
            return HttpResponse(jsstr, mimetype = 'application/json')

    if cmd == CMDAccount.userregister:
        jsstr = register(uname, passwd)
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDAccount.userlogin:
        jsstr = login(request, uname, passwd)
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDAccount.userlogout:
        jsstr = logout(request)
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDAccount.userunregister:
        jsstr = unRegister(request, uname, passwd)
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDAccount.order:
        orderlist = jsobj[1]['orderlist']
        jsstr = order(uname, passwd, orderlist)
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDAccount.unorder:
        instanceid = jsobj[1]['instanceid']
        jsstr = unOrder(uname, passwd, instanceid)
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDAccount.allapplist:
        jsstr = getAllAppList()
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDAccount.myapplist:
        jsstr = getMyAppList(uname, passwd)
        return HttpResponse(jsstr, mimetype = 'application/json')
    elif cmd == CMDAccount.appinfo:
        instanceid = jsobj[1]['instanceid']
        jsstr = getAppInfo(uname, passwd, instanceid)
        return HttpResponse(jsstr, mimetype = 'application/json')

def login(request, uname, passwd):
    """User request to auth into the system.
    """

    if not uname:
        return CMDAccount.ack_login(Status.FAIL, "user name can't be empty")
    if not passwd:
        return CMDAccount.ack_login(Status.FAIL, "password can't be empty.")

    user = auth.authenticate(username = uname, password = passwd)
    if user is not None:
        # Correct password

        if user.is_active:
            # the user is marked "active"
            # It's a valid user
            auth.login(request, user) #
            # login success
            return CMDAccount.ack_login(Status.SUCCESS,
                                    "authentication successfully")
        else:
            # the user is inactive
            return CMDAccount.ack_login(Status.FAIL,
                                    "disabled account")
    else:
        # Incorrect username or passwd
        return CMDAccount.ack_login(Status.FAIL,
                                    "invalid user name or password")

def logout(request):
    """User request to logout.

    @type request: HttpRequest
    @param request: When a page is requested, Django creates an HttpRequest
    object that contains metadata about the request.
    """
    auth.logout(request)
    return CMDAccount.ack_logout(Status.SUCCESS, "logout successfully")

def register(username, passwd):
    """User request to register as a valid account.
    """
    if not username:
        return CMDAccount.ack_register(Status.FAIL,
                                       "user name can't be empty")
    if not passwd:
        return CMDAccount.ack_register(Status.FAIL,
                                       "password can't be empty.")
    
    try:
        user = auth.models.User.objects.get(username = username)
        return CMDAccount.ack_register(Status.FAIL,
                                       "user %s exists." % username)
    except auth.models.User.DoesNotExist:
        user = auth.models.User.objects.create_user(username = username,
                                                    email = '',
                                                    password = passwd)
        # TODO. initial permission
        #user.user_permissions.add(...)
        user.save()
        return CMDAccount.ack_register(Status.SUCCESS,
                                       "register successfully")
    except auth.models.User.MultipleObjectsReturned:
        return CMDAccount.ack_register(Status.FAIL,
                              "internal err: multiple %s exist" % username)

def unRegister(request, username, passwd):
    """User request to unregister.
    """
    user = auth.authenticate(username = username, password = passwd)
    if user is not None:
        auth.logout(request)
        user.is_active = False
        user.groups.clear()
        user.user_permissions.clear()
        user.save()
        return CMDAccount.ack_unRegister(Status.SUCCESS, "successfully")
    else:
        return CMDAccount.ack_unRegister(Status.FAIL,
                                    "invalid user name or password")


def getMyAppList(username, passwd):
    """Get all the apps this user has ordered 
    """
    user = auth.authenticate(username = username, password = passwd)
    if user is not None:
        od_qs = Order.objects.filter(user = user)
        apps = []
        for app in od_qs:
            it = {"type": app.service.type,
                  "category": app.service.category,
                  "num": app.num, "state": app.state}
            apps.append(it)
        return CMDAccount.ack_getMyAppList(username, Status.SUCCESS,
                                           'successfully', apps)
    else:
        return CMDAccount.ack_getMyAppList(username, Status.FAIL,
                                           "invalid user name or password")
def getAllAppList():
    """ Get all of the app list published
    """
    apps = []
    for srv in Service.objects.all():
        it = {'type': srv.type, 'category': srv.category, 'logo': srv.logo,
              'description': srv.description}
        apps.append(it)
    return CMDAccount.ack_getAllAppList(Status.SUCCESS,
                                        'successfully', apps)

def getAppInfo(username, passwd, instanceid):
    """Get the information of user's specified app
    """
    user = auth.authenticate(username = username, password = passwd)
    if user is not None:
        od_qs = Order.objects.filter(user = user)
        od = None
        for i in od_qs:
            if i.instanceID() == instanceid:
                od = i
                break
        if not od:
            return CMDAccount.ack_getAppInfo(Status.FAIL,
                                  "instance %s doesn't exist % instanceid")
        info = {"type": od.service.type, "category": od.service.category,
                "logo": od.service.logo,
                "description": od.service.description, "state": od.state}

        if od.state == OrderState.RUNNING:
            info.update(spicehost = od.spicehost)
            info.update(spiceport = od.spiceport)

        return CMDAccount.ack_getAppInfo(Status.SUCCESS,
                                         "successfully", info)
    else:
        return CMDAccount.ack_getAppInfo(Status.FAIL,
                                         "invalid user name or password")

def order(username, passwd, orderlist):
    """User request an order,
    if successful, user will get the permission accordingly. 

    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type orderlist: list (that is [])
    @param orderlist: contain a list of service type to order
    """
    user = auth.authenticate(username = username, password = passwd)
    if user is not None:
        # check Service if valid orderlist
        for tp in orderlist:
            c = Service.objects.filter(type = tp).count()
            if c == 0:
                return CMDAccount.ack_order(Status.FAIL,
                               "invalid service type: %s" % tp)

        for tp in orderlist:
            srv = Service.objects.filter(type = tp)
            # get num
            od_qs = Order.objects.filter(user = user, service = srv[0])

            # There is at most one storage service per user,
            # If so, only ignore it but return success.
            if (srv[0].category == Service.CAT_DATA and od_qs.count() > 0):
                continue

            num = 0
            for od in od_qs:
                if od.num > num:
                    num = od.num

            num += 1

            new_od = Order(user = user, service = srv[0],
                           num = num, state = OrderState.ORDERED)
            new_od.save()
        
        return CMDAccount.ack_order(Status.SUCCESS, "successful")
    else:
        return CMDAccount.ack_order(Status.FAIL,
                                    "invalid user name or password")

def unOrder(username, passwd, instanceid):
    """User request cancel an order.

    @type username: str
    @param username: user name
    @type passwd: str
    @param passwd: password
    @type instanceid: str
    @param instanceid: the instance to cancel
    """
    user = auth.authenticate(username = username, password = passwd)
    if user is not None:
        od_qs = Order.objects.filter(user = user)
        od = None
        for i in od_qs:
            if i.instanceID() == instanceid:
                od = i
                break
        if not od:
            return CMDAccount.ack_unOrder(Status.FAIL,
                                  "instance %s doesn't exist" % instanceid)

        if od.state == OrderState.RUNNING:
            return CMDAccount.ack_unOrder(Status.FAIL,
                                "close the instance %s first" % instanceid)
        # TODO: request to release the resource of instanceid in host node
        od.delete()
        return CMDAccount.ack_unOrder(Status.SUCCESS, 'successful')
