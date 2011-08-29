#!/usr/bin/env python
#
# Filename: webfront/accounts/models.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
#
# -------------------------------------------------------------------
"""The authentication system use django's django.contrib.auth app.
There are 3 models in django.contrib.auth.models:
 * User
 * Permissions
 * Groups
This module will defined necessary models addtionally.
"""

from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    """The service provided, including vApp, vDesktop, server, fileman.
    The different params will be patched as different service

    @filed type: the service type or the name of the service
    @field category: 'DESKTOP', 'APPLICATION', 'DATA'
    @filed logo: the file name of logo picture (file path not included)
    @field description: introduce to this service
    @field price: The price of this service, reserved

    params below reserved for vDesktop or server
    @field disksize: reserved
    @field memsize: reserved
    @field netspeed: reserved
    @field cpunum: reserved
    """
    CAT_DESKTOP = 'DESKTOP'
    CAT_APP = 'APPLICATION'
    CAT_DATA = 'DATA'

    type = models.CharField(max_length = 50, primary_key = True)
    category = models.CharField(max_length = 15)
    logo = models.CharField(max_length = 50, null = True)
    description = models.CharField(max_length = 500, null = True)

class OrderState:
    """
    0-ordered, this service is in initial state, no resource allocated
    1-running, this service is running
    2-saved, this service is saved in snapshot and stoped
    3-stoped, this service stops running without snapshot,
              but the image kept
    4-canceled, this order is canceled, the image and snapshot are released
    """
    ORDERED = 0
    RUNNING = 1
    SAVED = 2
    STOPED = 3
    CANCELED = 4

class Order(models.Model):
    """User order
    @filed user: the user of this order
    @field sercive: the service of this order
    @field num: number of user's some service order,
                local to each user's each service type, begin with 0
    @field state:
        0-ordered, this service is in initial state, no resource allocated
        1-running, this service is running
        2-saved, this service is saved in snapshot and stoped
        3-stoped, this service stops running without snapshot,
                  but the image kept
        4-canceled, this order is canceled, the image and snapshot are released
    """

    user = models.ForeignKey(User)
    service = models.ForeignKey(Service)
    num = models.IntegerField()
    state = models.IntegerField()

    def instanceID(self):
        """get the name of the instance corresponding to an order record
        instanceid = username + type + num, so instanceid is gloal unique
        """
        instanceid = "%s%s%s" % (self.user.username,
                                 self.service.type, self.num)

        return instanceid

