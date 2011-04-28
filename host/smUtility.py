#!/usr/bin/env python
#
# Filename: host/smUtility.py
#
# -------------------------------------------------------------------
#
# 
#
# -------------------------------------------------------------------

def parseSplitFile(filename):
    """
    utility to read and parse a comma delimited file (meminfo)
    """
    f = open(filename, "rb")
    lines = f.readlines()
    del f

    lines = map(lambda x: x.strip().split(), lines)
    return lines
