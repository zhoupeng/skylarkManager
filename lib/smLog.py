#!/usr/bin/env python
#
# Filename: lib/smLog.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
# 
# -------------------------------------------------------------------
import inspect

def __function__():
    caller = inspect.stack()[1]
    return caller[3]

def __line__():
    caller = inspect.stack()[1]
    return int (caller[2])

