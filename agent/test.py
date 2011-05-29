#!/usr/bin/env python
#
# Filename: agent/test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------

if __name__ == '__main__':

    import smListeners
    hostListener = smListeners.Listener(port = 1234, type = "host")
    hostListener.start()

    # test scheduler

    # M_MEM
    from smGlobals import *
    from smSchedule import Scheduler
    sched = Scheduler.getInstance()
    #sched.setMethod(Scheduler.M_MEM)
    sched.setMethod(Scheduler.M_CPU)
    import time
    time.sleep(60)
    print sched.getMethod()
    sched.schedule(hosts)
    #print hosts
    hosts.dump()
    time.sleep(30)
    print sched.getMethod()
    sched.schedule(hosts)
    #print hosts
    hosts.dump()

    hostListener.join()
