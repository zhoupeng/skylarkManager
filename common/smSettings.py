#
#
# Filename: common/settings.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.06 ~
#
# -------------------------------------------------------------------

""" This is the configuration file, user should modify the fields,
according to the real system deployment.
"""

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

# Famous ports
CLIENTSRV_PORT = 5990
MASTER_AGENT_PORT = 5991

# Well known host interface

# WEB_FRONT_URL = ''
