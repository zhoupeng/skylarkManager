#!/usr/bin/env python
#
# Filename: common/CONSTANTS.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------

# host types
XENHOST = "xen"
KVMHOST = "kvm"

# How long to report host resource once
RS_REPORT_INTERVAL = 30

VTYPE_STRING = 'string'
VTYPE_MAYBE_STRING = "maybe-string"
VTYPE_BOOL = 'bool'
VTYPE_SIZE = 'size' # size, in MiBs
VTYPE_INT = 'int'

# HV parameter names (global namespace)
HV_KERNEL_PATH = "/usr/lib/xen/boot/hvmloader"
HV_DEVICE_MODEL = "/usr/lib/xen/bin/qemu-dm"

#HV_VM_CONFIG_PATH = "/etc/skylark/config"
#HV_DISK_IMG_PATH = "/etc/skylark/imgs"
HV_VM_CONFIG_PATH = "/home/zp/Desktop/fc8/hvm-WinXP"
HV_DISK_IMG_PATH = "/home/zp/Desktop/fc8/hvm-WinXP"

