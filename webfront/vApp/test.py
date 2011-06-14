#!/usr/bin/env python
#
# Filename: webfront/vApp/test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
#
# -------------------------------------------------------------------
""" Ack as http client
"""

"""
urllib.request.urlopen(url, data=None[, timeout])

the HTTP request will be a POST instead of a GET 
when the data parameter is provided.
data should be a buffer in the standard 
application/x-www-form-urlencoded format.

The optional timeout parameter specifies a timeout in seconds 
for blocking operations like the connection attempt 
(if not specified, the global default timeout setting will be used).
This actually only works for HTTP, HTTPS and FTP connections.
"""
import libconf2

import urllib
import urllib2

from smCMD import *
from django.utils import simplejson as json

urlroot = 'http://192.168.1.187:8000'
url = "%s/vappreq" % urlroot


"""
headers = {"Content-Type": "application/x-www-form-urlencoded"}

type = 'fedora14'
jsobj = CMDClientAgent.cmd_reqinstance(type)
values = {'name': 'Michael Foord',
          'location': 'Northampton',
          'language': 'Python'}

#data = urllib.urlencode(jsobj) # TypeError: not a valid non-string sequence or mapping object
#data = urllib.urlencode({'req': jsobj}) # POST #ok
data = urllib.urlencode(values) # POST #ok
print data
print type(data)

#req = urllib2.Request(url, data) # POST #ok
#req = urllib2.Request(url, data, {"Content-Type": "application/json"}) # POST # ok
#req = urllib2.Request(url, data, headers) # POST # ok 
"""


""" This is ok to send json str as content.
type = 'fedora14'
jsobj = CMDClientAgent.cmd_reqinstance(type)
req = urllib2.Request(url, jsobj, {"Content-Type": "application/x-www-form-urlencoded"})
resp = urllib2.urlopen(req)
"""


""" This is ok to send json str as content.
type = 'fedora14'
jsobj = CMDClientAgent.cmd_reqinstance(type)
req = urllib2.Request(url, jsobj, {"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
"""

""" This is ok to send json str as content.
from django.utils import simplejson as json
type = 'fedora14'
#jsobj = CMDClientAgent.cmd_reqinstance(type)
jsobj = json.dumps({"username":"ZZZZZZZZ", "password":"**********"})
req = urllib2.Request(url, jsobj, {"Content-Type": "text/plain", "Accept-Type": "application/json"})
resp = urllib2.urlopen(req)
"""


""" This is ok to send json str as content.
type = 'fedora14'#'UserVMxpPro'
jsobj = CMDClientAgent.cmd_reqinstance(type)
req = urllib2.Request(url, jsobj)
resp = urllib2.urlopen(req)
"""


#""" This is ok to send json str as content.
type = 'fedora14'
#type = 'UserVMxpPro'
jsobj = CMDClientAgent.cmd_reqinstance(type)
resp = urllib2.urlopen(url, jsobj)
#"""


page = None
if resp:
    global page
    page = resp.read()

print "resp.read()..........."
print page

