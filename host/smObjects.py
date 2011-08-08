#!/usr/bin/env python
#
# Filename: host/smObjects.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.05 ~
#
# -------------------------------------------------------------------

"""This module provides small, mostly data-only objects.
"""

from CONSTANTS import *
from time import time
import smIO

class Instance:
    """Config object representing an instance.
    This class can be extented to store more info about an vm, which
    can be accessed by getinstanceinfo
    """

    def __init__(self, name, spicehost, spiceport, owner = None,
                 type = None, nth = 0):
        """
        @type name: str
        @params name: vm name
        @type spiceport: int
        @params spiceport: listen port
        @type owner: str
        @params owner: the owner of vm
        @type type: str
        @params type: instance type, served for(winxp, linux, word ...)
        @type nth: str
        @params nth: how many instance now('1', '2' ...)
        @type uuid: str
        @params uuid: the uuid of this instance
        @type state: str
        @params state: the state of the instance
        """

        self.name = name
        self.spicehost = spicehost
        self.spiceport = spiceport
        self.uuid = smIO.NewUUID()
        self.owner = owner
        self.type = type
        self.nth = nth
        self.timestamp = time()
        self.state = None

