#
#
# Filename: common/smSettings.py
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
HOST_TYPE = "xen" # "kvm", "xen"

# HV parameter names
HV_KERNEL_PATH = "/usr/lib/xen/boot/hvmloader"
HV_DEVICE_MODEL = "/usr/lib/xen/bin/qemu-dm"

#HV_VM_CONFIG_PATH = "/etc/skylark/config"
#HV_DISK_IMG_PATH = "/etc/skylark/imgs"
HV_VM_CONFIG_PATH = "/home/zp/Desktop/fc8/hvm-WinXP"
HV_DISK_IMG_PATH = "/home/zp/Desktop/fc8/hvm-WinXP"

# Famous ports
CLIENTSRV_PORT = 6000
MASTER_AGENT_PORT = 6001

# Well known host interface
CLIENTSRV_HOST = '192.168.1.187'
MASTER_AGENT_HOST = '192.168.1.187'

# used by Agent to query info from (send req to) the webfront if necessary
WEB_FRONT_URL = 'http://192.168.1.187:8000'

# NICs
# NI to use for spice server on host
SPICE_NI = 'eth0' # 'lo', 'ethx'
