#!/usr/bin/env python
#
# Filename: host/libconf.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------
"""
Adding lib and common to the python path
"""
import sys
import os
lib_path = os.path.abspath('../lib')
common_path = os.path.abspath('../common')
sys.path.append(lib_path)
sys.path.append(common_path)
