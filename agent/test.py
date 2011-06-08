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
import libconf
from CONSTANTS import *
if __name__ == '__main__':

    import smListeners
    hostListener = smListeners.Listener(port = MASTER_AGENT_PORT, type = "host")
    hostListener.start()

    from CONSTANTS import *
    import smClient
    clientSrv = smClient.Client(port = CLIENTSRV_PORT, host = CLIENTSRV_HOST)
    clientSrv.start()

    """
    # test scheduler

    # M_MEM
    from smGlobals import *
    from smSchedule import Scheduler
    sched = Scheduler.getInstance()
    #sched.setMethod(Scheduler.M_MEM)
    #sched.setMethod(Scheduler.M_CPU)
    sched.setMethod(Scheduler.M_CYCLIC)
    import time
    time.sleep(60)
    print sched.getMethod()
    print sched.schedule(hosts)
    #print hosts
    hosts.dump()
    time.sleep(30)
    print sched.getMethod()
    print sched.schedule(hosts)
    #print hosts
    hosts.dump()
    """
    hostListener.join()
    clientSrv.join()
