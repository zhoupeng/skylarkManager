#!/usr/bin/env python
#
# Filename: modstest/sxt_test.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.10 ~
#
# -------------------------------------------------------------------
import libconf

import smSXP as sxp
from StringIO import StringIO

buf = '(domain (domid 8) (cpu_weight 256) (cpu_cap 0) (on_crash restart) (uuid c0e968c2-4bd0-ceab-bec1-84cbc6d03b76) (bootloader_args) (vcpus 1) (name fedora14) (on_poweroff destroy) (on_reboot restart) (cpus (())) (description) (bootloader) (maxmem 300) (memory 300) (shadow_memory 4) (vcpu_avail 1) (features) (on_xend_start ignore) (on_xend_stop ignore) (start_time 1307676359.57) (cpu_time 14.629698989) (online_vcpus 1) (image (hvm (kernel) (superpages 0) (tsc_mode 0) (videoram 4) (hpet 0) (boot c) (loader /usr/lib/xen/boot/hvmloader) (spicehost 192.168.1.187) (serial pty) (spiceport 0062) (vpt_align 1) (xen_platform_pci 1) (vncunused 1) (rtc_timeoffset 0) (pci ()) (pae 1) (stdvga 0) (hap 1) (spice 1) (viridian 0) (acpi 1) (localtime 0) (timer_mode 1) (vnc 1) (spice_disable_ticketing 1) (nographic 0) (guest_os_type default) (pci_msitranslate 1) (oos 1) (apic 1) (nomigrate 0) (usbdevice tablet) (device_model /usr/lib/xen/bin/qemu-dm) (spiceagent_mouse 1) (pci_power_mgmt 0) (usb 0) (xauthority /root/.xauthn6GhR4) (isa 0) (display :0.0) (notes (SUSPEND_CANCEL 1)))) (status 2) (state -b----) (store_mfn 1044476) (device (vbd (uuid 428676ef-d10b-5bee-3546-2059ee3f40b6) (bootable 1) (dev hda:disk) (uname file:/home/zp/Desktop/fc8/hvm-WinXP/fedora14.img) (mode w) (backend 0) (VDI))) (device (vfb (vncunused 1) (vnc 1) (uuid 1758a9e8-7d6a-1eea-ef65-706d0fde89ae) (location 127.0.0.1:5900))) (device (console (protocol vt100) (location 3) (uuid f25d3a7c-e937-b7bb-087e-5ba62bb27975))))'

strio = StringIO(buf)
sxp_obj = sxp.parse(strio)
print "type(sxp_obj): %s" % type(sxp_obj)
print "\nsxp_obj[0]:\n %s" % sxp_obj[0]
print "\nsxp_obj:\n %s" % sxp_obj
print "\nshow(sxp_obj):"
sxp.show(sxp_obj)
print "\nshow(sxp_obj[0]):"
sxp.show(sxp_obj[0])

print "\nname(sxp_obj[0]):"
print sxp.name(sxp_obj[0])

print "\nattributes(sxp_obj[0]):"
print sxp.attributes(sxp_obj[0])

print "\nsxp.children(sxp_obj)"
print sxp.children(sxp_obj)

print "\nchildren(sxp_obj[0])"
print sxp.children(sxp_obj[0])

print "\nchildren(sxp_obj[0], 'domid')"
print sxp.children(sxp_obj[0], 'domid')

print "\nchildren(sxp_obj[0], 'image')"
print sxp.children(sxp_obj[0], 'image')

print "\nchild(sxp_obj[0], 'domid')"
print sxp.child(sxp_obj[0], 'domid')


print "\nsxp.child(sxp.child(sxp.child(sxp_obj[0], 'image'), 'hvm'), 'spiceport')"
print sxp.child(sxp.child(sxp.child(sxp_obj[0], 'image'), 'hvm'), 'spiceport')
print sxp.child(sxp.child(sxp.child(sxp_obj[0], 'image'), 'hvm'), 'spicehost')
print sxp.child_value(sxp.child(sxp.child(sxp_obj[0], 'image'), 'hvm'), 'spicehost')

print "sxp.child_with_id(sxp_obj, 'spicehost')"
print sxp.child_with_id(sxp_obj, 'spicehost')

print "sxp.elements(sxp_obj)"
print type(sxp.elements(sxp_obj))
print str(sxp.elements(sxp_obj))

# I add child_with_element
print "sxp.child_with_element(sxp_obj[0], 'spiceport')"
print sxp.child_with_element(sxp_obj[0], 'spiceport')
print "sxp.child_with_element(sxp_obj[0], 'spiceport')[1]"
print sxp.child_with_element(sxp_obj[0], 'spiceport')[1]

