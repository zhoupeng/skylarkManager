#!/usr/bin/env python
#
# Filename: lib/smCPUUsage.py
#
# -------------------------------------------------------------------
#
#  Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
import time

class CPUsage:
    """calculate cpu usage for Linux system via /proc interface
    """

    def __init__(self, interval = 0.1):
        self._interval = interval # second
        self._cpurate = 0.0
        self._cpusec = 0 # milliseconds
        self.recompute()

    @staticmethod
    def get_time():
        stat_file = file("/proc/stat", "r")
        time_list = stat_file.readline().split(" ")[2:6]
        stat_file.close()
        for i in range(len(time_list)):
            time_list[i] = int(time_list[i])
        return time_list
    
    def delta_time(self):
        x = self.get_time()
        time.sleep(self._interval) # default 0.1 second(100ms)
        y = self.get_time()
        for i in range(len(x)):
            y[i] -= x[i]
        return y
    
    def recompute(self):
        t = self.delta_time()
        self._cpurate = 100 - (t[len(t) - 1] * 100.00 / sum(t))
        self._cpusec = sum(t)

    def getcpurate(self):
        return self._cpurate
    
    def getcpusec(self):
        return self._cpusec

    def __repr__(self):
        return str({'cpurate': self._cpurate, 'cpusec': self._cpusec})

