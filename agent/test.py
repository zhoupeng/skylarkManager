#!/usr/bin/env python
#
# Filename: agent/test.py
#
# -------------------------------------------------------------------
#
# 
#
# -------------------------------------------------------------------

if __name__ == '__main__':

    import smListeners
    hostListener = smListeners.Listener(port = 1234, type = "host")
    hostListener.start()
    hostListener.join()