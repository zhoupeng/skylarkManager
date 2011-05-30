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
    """Config object representing an instance."""

    def __init__(self, name, spicehost, spiceport, type = "winxp"):
        """
        @type name: str
        @params name: vm name
        @type spiceport: int
        @params spiceport: listen port
        @type type: str
        @params type: instance type, served for(winxp, linux, word ...)
        @type uuid: str
        @params uuid: the uuid of this instance
        @type state: str
        @params state: the state of the instance
        """

        self.name = name
        self.spicehost = spicehost
        self.spiceport = spiceport
        self.uuid = smIO.NewUUID()
        self.type = type
        self.timestamp = time()
        self.state = None

