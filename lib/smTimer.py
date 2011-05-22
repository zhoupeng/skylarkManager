#!/usr/bin/env python
#
# Filename: lib/smUtility.py
#
# -------------------------------------------------------------------
#
#  Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.05 ~
#
# -------------------------------------------------------------------
import threading
import time
import smErrors as errors

class PerpetualTimer(threading._Timer):
    """A responsive subclass of threading._Timer whose run() method repeats.
    
    Use this timer only when you really need a very interruptible timer;
    this checks its 'finished' condition up to 20 times a second, which can
    results in pretty high CPU usage
    """
    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.isSet():
                return
            try:
                self.function(*self.args, **self.kwargs)
            except Exception, x:
                emsg = "Error in perpetual timer thread function %r." % self.function
                raise errors.GenericError(emsg)


class BackgroundTask(threading.Thread):
    """A subclass of threading.Thread whose run() method repeats.
    
    Use this class for most repeating tasks. It uses time.sleep() to wait
    for each interval, which isn't very responsive; that is, even if you call
    self.cancel(), you'll have to wait until the sleep() call finishes before
    the thread stops. To compensate, it defaults to being daemonic, which means
    it won't delay stopping the whole process.
    """
    def __init__(self, interval, function, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.running = False
   
    def cancel(self):
        self.running = False
   
    def run(self):
        self.running = True
        while self.running:
            time.sleep(self.interval)
            if not self.running:
                return
            try:
                self.function(*self.args, **self.kwargs)
            except Exception, err:
                emsg = ("Error in background task thread function %r, error: %s."
                        % (self.function, err))
                raise errors.GenericError(emsg)
   
    def _set_daemon(self):
        return True
