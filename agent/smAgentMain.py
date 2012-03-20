#!/usr/bin/env python
#
# Filename: agent/smAgentMain.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2012.03 ~
#
# -------------------------------------------------------------------
import libconf
from CONSTANTS import *
import smListeners
import smClient
from smSchedule import Scheduler

if __name__ == '__main__':
    hostListener = smListeners.Listener(port = MASTER_AGENT_PORT,
                                        type = "host")
    hostListener.start()

    clientSrv = smClient.Client(port = CLIENTSRV_PORT,
                                host = CLIENTSRV_HOST)
    clientSrv.start()

    sched = Scheduler.getInstance()
    sched.setMethod(Scheduler.M_CYCLIC)
    hostListener.join()
    clientSrv.join()
