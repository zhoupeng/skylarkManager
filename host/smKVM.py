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
from cStringIO import StringIO
import datetime
from smVirshXML import *

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

    def createInstance1(self, vmName, spicehost, spiceport,
                       memory = 300):
        """Create a VM through qemu-kvm cmd directly.
        NB. Obsolete
        """
        runtime = self.generateKVMRuntime(vmName, spicehost, spiceport, memory)
        self.saveKVMRuntime(vmName, runtime)

        res = utilsProcess.RunCmd(runtime)

        if res.failed:
            print "KVM create VM fails, reason:%s" % res.fail_reason
            return None
        
        ins = smObjects.Instance(vmName, spicehost, spiceport)

        return ins

    @classmethod
    def _writeConfigFile(cls, vmName, spicehost, spiceport,
                        memory = 300, xml = None):
        """ Create a hvm config file.
        If xml is not None, the xml is writen into the cfg file,
        else the default value.

        @type xml: str
        @param xml: xml string provided by caller
        """ 
        config = StringIO()

        config.write("<!--\n")
        config.write("%s\n" % datetime.datetime.now())
        config.write(
            "This is auto-generated by skylarkhost, please don't edit.\n")
        config.write("-->\n")

        if xml:
            config.write(xml)
        else:
            diskimgpath = "%s/%s.img" % (HV_DISK_IMG_PATH, vmName)
            config.write("""
<domain type='kvm'>
    <name>%s</name>
    <memory>%s</memory>
    <vcpu>1</vcpu>
    <os>
        <type arch='x86_64' machine='pc'>hvm</type>
    </os>
    <features>
        <acpi/>
        <apic/>
        <pae/>
    </features>
    <on_poweroff>destroy</on_poweroff>
    <devices>
        <emulator>%s</emulator>
        <disk type='file' device='disk'>
            <source file='%s'/>
            <target dev='hda' bus='ide'/>
        </disk>
        <graphics type='spice' listen='%s' port='%s'/>
        <video>
            <model type='qxl'/>
        </video>
    </devices>
</domain>
""" % (vmName, memory * 1024, KVM_PATH, diskimgpath, spicehost, spiceport))

        smIO.RemoveFile("%s/%s.xml" % (HV_VM_CONFIG_PATH, vmName))

        try:
            smIO.WriteFile("%s/%s.xml" % (HV_VM_CONFIG_PATH, vmName),
                           data = config.getvalue())
        except EnvironmentError, err:
            raise errors.HypervisorError("Cannot write KVM instance XML"
                                   " file %s/%s.xml: %s" %
                                   (HV_VM_CONFIG_PATH, vmName, err))

        return True

    def createInstance(self, vmName, spicehost, spiceport,
                       memory = 300):
        """Create or start a VM through virsh.
        """
        self._writeConfigFile(vmName, spicehost, spiceport, memory)

        cmd = VIRSH_PATH if VIRSH_PATH else 'virsh'
        res = utilsProcess.RunCmd([cmd, "create", "%s/%s.xml" % 
                                  (HV_VM_CONFIG_PATH, vmName)])
        if res.failed:
            print "virsh create fails, reason:%s" % res.fail_reason
            return None
        
        ins = smObjects.Instance(vmName, spicehost, spiceport)

        return ins

    def newInstanceBySnapshot(self, vmName, spicehost, spiceport):
        """Create a VM from checkpoint template file
        Use our storage system to parse vmName
        """
        # General and proper way(compatible with general fs
        # and my coming dfs shared fs):
        # Have a copy from the checkpoint file template,
        # have a copy from the disk img template,
        # and adjust the necessary params of xml header
        # then restore from the copy?
        # Here we use skyalrk storage to tuning temporarily.
        ckp = "%s/%s.ckp" % (HV_CKP_TEMPLATE_PATH, vmName)
        ins = self._runVirshRestore(ckp, vmName, spicehost, spiceport)
        return ins

    @staticmethod
    def _runVirshRestore(ckpfile, vmName, spicehost,
                         spiceport, xml = None):
        """Helper function for L{newInstanceBySnapshot, restoreInstance}
        to run "virsh restore".
        Assume checkpointfile is ready
        
        @type ckpfile: str
        @param: the file name of the checkpoint,
         including the complete path, otherwish the current dir 
        @type xml: str
        @param: The file name of an alternative xml used to pass changes,
         xml including the complete file path, otherwish the current dir
        """
        virsh = VIRSH_PATH if VIRSH_PATH else 'virsh'
        cmd = [virsh, "restore", ckpfile]
        optxml = ["--xml", xml] if xml else None
        if optxml:
            cmd.extend(optxml)
        res = utilsProcess.RunCmd(cmd)
        
        if res.failed:
            print "KVM restore fails, reason:%s, extra: %s" % (
                                            res.fail_reason,
                                            res.stderr)
            return None
        
        ins = smObjects.Instance(vmName, spicehost, spiceport)

        return ins

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
        vmxml = "%s/%s.xml" % (HV_VM_CONFIG_PATH, vmName)
        # Adjust(modify) the spiceport(host) fields of the xml file
        vvmxml = VirshVMXML()
        if not vvmxml.init(vmxml):
            return None
        options = {VirshOptions.SPICEHOST: spicehost,
                   VirshOptions.SPICEPORT: str(spiceport)}
        if not vvmxml.adjust(**options):
            return None

        ckp = "%s/%s.ckp" % (HV_DISK_IMG_PATH, vmName)

        ins = self._runVirshRestore(ckp, vmName, spicehost,
                                    spiceport, vmxml)
        return ins

    @staticmethod
    def _runVirshDumpxml(instanceid):
        """Get KVM VM's xml config info through virsh dumpxml

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """
        virsh = VIRSH_PATH if VIRSH_PATH else 'virsh'
        res = utilsProcess.RunCmd([virsh, "dumpxml", instanceid])

        if res.failed:
            print "KVM dumpxml %s failed, reason:%s, extra: %s" % (
                                                        instanceid,
                                                        res.fail_reason,
                                                        res.stderr)
            return None

        return res.stdout

    @staticmethod
    def _runVirshShutdownInstance(instanceid):
        """ Helper function for L{shutdownInstance}

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """
        virsh = VIRSH_PATH if VIRSH_PATH else 'virsh'
        res = utilsProcess.RunCmd([virsh, "destroy", instanceid])

        if res.failed:
            print "KVM shutdown %s failed, reason:%s" % (instanceid,
                                                        res.fail_reason)
            return None
        return res

    def shutdownInstance(self, instanceid):
        """ shutdown the vm instance (instanceid)

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """
        return self._runVirshShutdownInstance(instanceid)

    @staticmethod
    def _runVirshSave(instanceid, ckpfile):
        """ Helper function for L{saveInstance}

        @type instanceid: str
        @param instanceid: the actual name of an instance
        @type ckpfile: str
        @param ckpfile: the file to save the checkpoint,
        including the complete path, otherwish the current dir 
        """
        virsh = VIRSH_PATH if VIRSH_PATH else 'virsh'
        res = utilsProcess.RunCmd([virsh, "save", instanceid, ckpfile])

        if res.failed:
            print "KVM save %s failed, reason:%s, extra: %s" % (instanceid,
                                                    res.fail_reason,
                                                    res.stderr)
            return None
        return res

    def saveInstance(self, instanceid):
        """ save the vm instance (instanceid)

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """
        ckpfile = "%s/%s.ckp" % (HV_DISK_IMG_PATH, instanceid)
        # calculate the real vm name to meet skylark storage
        # calculate instance name(instance id)
        # we'll use consistent instanceid
        # (just pass as a paremeter),
        # when skylark storage get transparent

        #import uuid
        #import md5
        #instanceid = str(uuid.UUID(bytes = md5.new(instanceid).digest())) 

        # Update the vm xml config file used by restore later.
        # The restore pass parameter based on this xml.
        # Thanks to virsh restore to avoid modify the ckp directly.
        self._writeConfigFile(instanceid, None, 0,
                xml = self._runVirshDumpxml(instanceid))

        return self._runVirshSave(instanceid, ckpfile)

    def verify(self):
        """Verify the hypervisor.

        Check that the binary exists.

        """
        raise NotImplementedError
        #if not os.path.exists(constants.KVM_PATH):
        #    return "The kvm binary ('%s') does not exist." % constants.KVM_PATH
        #if not os.path.exists(constants.SOCAT_PATH):
        #    return "The socat binary ('%s') does not exist." % constants.SOCAT_PATH

