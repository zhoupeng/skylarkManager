#!/usr/bin/env python
#
# Filename: host/smKVM.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
import libconf

from CONSTANTS import *
import smBase
import os
import smIO
import smErrors as errors
import simplejson as json
import smProcess as utilsProcess
import smObjects

class KVMNode(smBase.BaseHypervisor):

    def getType(self):
        return KVM_TYPE

    def getCPUUsage(self):
        """Get the cpu usage.

        @return: a dict with the following keys:
         - cpusec: the cpu consumed in milliseconds in the measure interval
         - cpurate: the cpu usage percentage in the measure interval
        """
        return self.getLinuxCPUUsage()

    def getNodeInfo(self):
        """Return information about the node.

        @return: a dict with the following keys (memory values in MiB):
            - memory_total: the total memory size on the node
            - memory_free: the available memory on the node for instances
            - memory_dom0: the memory used by the node itself, if available
            - nr_cpus(cpu_total): total number of CPUs
            - nr_nodes(cpu_nodes): in a NUMA system, the number of domains
            - nr_sockets(cpu_sockets): the number of
                                       physical CPU sockets in the node

        """
        return self.getLinuxNodeInfo()

    def generateKVMRuntime(self, vmName, spicehost, spiceport,
                           memory = 300):
        """Generate KVM cmd with args
        """
        kvm = KVM_PATH
        kvm_cmd = [kvm]

        kvm_cmd.extend(["-m", memory])
        kvm_cmd.extend(["-name", vmName])
        kvm_cmd.extend(["-enable-kvm"])

        disk_img = "%s/%s.img" % (HV_DISK_IMG_PATH, vmName)
        # if=virtio leads to crashing of installed win7 by xen
        #drive = "file=%s,if=virtio" % disk_img 
        drive = "file=%s" % disk_img
        kvm_cmd.extend(["-drive", drive])

        kvm_cmd.extend(["-vga", "qxl"])

        #kvm_cmd.extend(["-pidfile", pidfile])
        kvm_cmd.extend(["-daemonize"])

        spice_arg = "addr=%s,port=%s,disable-ticketing" % (spicehost,
                                                           spiceport)
        kvm_cmd.extend(["-spice", spice_arg])
        
        '''* Improve the experience by enable spice agent communication
        channel between the host and the guest(including copy and past).
        NB. The guest need to install and run agent client.
        * It's important that the virserialport chardev= option matches
        the <cdoe>id=</code> given the chardev (vdagentchannel in this
        example).
        It's also important that the port's name= is com.redhat.spice.0,
        because that's the namespace spice-vdagentd is looking for
        in the guest.
        And finally, you need to specify name=vdagent so spice knows
        what this channel is for.'''
        # Add the virtio-serial device.
        kvm_cmd.extend(["-device", "virtio-serial-pci"])
        # Add a port for spice in that device.
        virtserialport = (
           "virtserialport,chardev=vdagentport,name=com.redhat.spice.0")
        kvm_cmd.extend(["-device", virtserialport])
        # Add a spicevmc chardev for that port.
        spicevmc = "spicevmc,id=vdagentport,name=vdagent"
        kvm_cmd.extend(["-chardev", spicevmc])

        return kvm_cmd

    def saveKVMRuntime(self, vmName, runtime):
        """Save the runtime in the cfg dir

        @type vmName: str
        @param vmName: The name of the vm instance
        @type runtime: list
        @param runtime: qemu-kvm comand line
        """
        smIO.RemoveFile("%s/%s.cfg" % (HV_VM_CONFIG_PATH, vmName))

        try:
            smIO.WriteFile("%s/%s.cfg" % (HV_VM_CONFIG_PATH, vmName),
                           data = json.dumps(runtime))
        except EnvironmentError, err:
            raise errors.HypervisorError("Cannot write KVM instance confile"
                                   " file %s/%s.cfg: %s" %
                                   (HV_VM_CONFIG_PATH, vmName, err))

    def createInstance(self, vmName, spicehost, spiceport,
                       memory = 300):
        """Create a VM
        """
        runtime = self.generateKVMRuntime(vmName, spicehost, spiceport, memory)
        self.saveKVMRuntime(vmName, runtime)

        res = utilsProcess.RunCmd(runtime)

        if res.failed:
            print "KVM create VM fails, reason:%s" % res.fail_reason
            return None
        
        ins = smObjects.Instance(vmName, spicehost, spiceport)

        return ins

    def newInstanceBySnapshot(self, vmName, spicehost, spiceport):
        """Create a VM from checkpoint template file
        Use our storage system to parse vmName
        """
        pass

    def restoreInstance(self, vmName, spicehost, spiceport):
        """Restore a VM from it's own checkpoint file
        Don't use and allow the storage system to parse vmName, keep
        the same as you see.
        Assume the vm's checkpoint file is saved before

        @type vmName: str
        @param vmName: the actual name of an instance
        @type spicehost: str
        @param spicehost: This host's ip for this spice server
        @type spiceport: int
        @param spiceport: the port for this spice server
        """
        pass

    def shutdownInstance(self, instanceid):
        """ shutdown the vm instance (instanceid)

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """

    def saveInstance(self, instanceid):
        """ save the vm instance (instanceid)

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """

    def verify(self):
        """Verify the hypervisor.

        Check that the binary exists.

        """
        raise NotImplementedError
        #if not os.path.exists(constants.KVM_PATH):
        #    return "The kvm binary ('%s') does not exist." % constants.KVM_PATH
        #if not os.path.exists(constants.SOCAT_PATH):
        #    return "The socat binary ('%s') does not exist." % constants.SOCAT_PATH

