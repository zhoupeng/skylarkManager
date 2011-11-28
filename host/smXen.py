#!/usr/bin/env python
#
# Filename: host/smXen.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.04 ~
#
# -------------------------------------------------------------------

"""
support xen list:
* xen 4.0.1 with xm tools
* The xen before 4.0.1 with compatible xm tools 
"""
import libconf

import smProcess as utilsProcess
import smRetry as utilsRetry
import smErrors as errors
from CONSTANTS import *
import logging
from cStringIO import StringIO
import smIO
import smObjects
import datetime
from smCheckpoint import *

class XenNode(object):

    def getMemInfo(self):
        pass

    def getType(self):
        return XEN_TYPE

    def getCPUUsage(self):
        xentop = self._getXentop()

        cpuusage = {}
        cpuusage['cpusec'] = 0
        cpuusage['cpurate'] = 0.0

        for ele in xentop:
            cpuusage['cpurate'] += ele[3]
            cpuusage['cpusec'] += ele[2]

        return cpuusage
        

    @staticmethod
    def _runXentop(xentop_errors, it = 2, delay = 1):
        """Helper function for L{_getXentop} to run "xentop -i $it -b"

        @type it: int
        @param it: iteration count, must >= 2
        @type delay: float
        @param delay: seconds between updates(default of xentop 3)
        @rtype: list of tuples
        @return: $it iteration results.
        """
        result = utilsProcess.RunCmd(["xentop", "-i", it, "-b", "-d", delay])
        return result.stdout.splitlines()

    @classmethod
    def _getXentop(cls, it = 2, delay = 1):
        """Return the last iteration of xentop.

        @type it: int
        @param it: iteration count, must >= 2
        @type delay: float
        @param delay: seconds between updates(default of xentop 3)
        @rtype: list of tuples
        @return: list of (NAME STATE CPU(sec) CPU(%) MEM(k) MEM(%) MAXMEM(k) MAXMEM(%) 
        VCPUS NETS NETTX(k) NETRX(k) VBDS VBD_OO VBD_RD VBD_WR VBD_RSECT VBD_WSECT SSID)
        """
        xentop_errors = []
        try:
            lines = utilsRetry.Retry(cls._runXentop, 
                       1, 5, args=(xentop_errors, it, delay))
        except utilsRetry.RetryTimeout:
            if xentop_errors:
                xentop_result = xentop_errors.pop()
                errmsg = ("xentop failed, timeout exceeded (%): %s" %
                           (xentop_result.fail_reason, xentop_result.output))
            else:
                errmsg = "xentop -i %d -b -d %0.1f failed" % (it, delay)
            raise errors.HypervisorError(errmsg)

        # keep the last iteration and 
        # skip over the heading
        lines.reverse()
        lines = lines[:lines.index("      NAME  STATE   CPU(sec) CPU(%)     \
MEM(k) MEM(%)  MAXMEM(k) MAXMEM(%) VCPUS NETS NETTX(k) NETRX(k) VBDS   VBD_OO\
   VBD_RD   VBD_WR  VBD_RSECT  VBD_WSECT SSID")]

        # clean up 'no limit' string of dom0 max mem
        # clean up 'n/a' string of MAXMEM(%) 
        lines.reverse()
        #lines[0] = lines[0].replace("no limit", "0")
        #lines[0] = lines[0].replace("n/a", "0")
        for i in range(0, len(lines)):
            lines[i] = lines[0].replace("no limit", "0")
            lines[i] = lines[0].replace("n/a", "0")
       
        result = []
        for line in lines:
            # format of line
            # NAME STATE CPU(sec) CPU(%) MEM(k) MEM(%) MAXMEM(k) MAXMEM(%) VCPUS 
            # NETS NETTX(k) NETRX(k) VBDS VBD_OO VBD_RD VBD_WR VBD_RSECT VBD_WSECT SSID
            data = line.split()
            if len(data) != 19:
                raise errors.HypervisorError("Can't parse output of xentop,"
                                             "line: %s" % line)
            try:
                data[2] = long(data[2]) # CPU(sec)
                data[3] = float(data[3]) # CPU(%)
                data[4] = long(data[4]) # MEM(k)
                data[5] = float(data[5]) # MEM(%)
                data[6] = long(data[6]) # MAXMEM(k)
                data[7] = float(data[7]) # MAXMEM(%)
                data[8] = int(data[8]) # VCPUS
                data[9] = int(data[9]) # NETS
                data[10] = int(data[10]) # NETTX(k)
                data[11] = int(data[11]) # NETRX(k)
                data[12] = int(data[12]) # VBDS
                # ... ignore
            except (TypeError, ValueError), err:
                raise errors.HypervisorError("Can't parse output of xentop,"
                                             " line: %s, error: %s" % (line, err))
            result.append(data)

        return result


    @staticmethod
    def _runXmList(xmlist_errors):
        """Helper function for L{_getXMList} to run "xm list".

        """
        result = utilsProcess.RunCmd(["xm", "list"])
        
        # skip over the heading
        return result.stdout.splitlines()[1:]

    @classmethod
    def _getXMList(cls, include_node):
        """Return the list of running instances.

        If the include_node argument is True, then we return information
        for dom0 also, otherwise we filter that from the return value.

        @return: list of (name, id, memory, vcpus, state, time spent)

        """
        xmlist_errors = []
        try:
            lines = utilsRetry.Retry(cls._runXmList, 1, 5, args=(xmlist_errors, ))
        except utilsRetry.RetryTimeout:
            if xmlist_errors:
                xmlist_result = xmlist_errors.pop()

                errmsg = ("xm list failed, timeout exceeded (%s): %s" % 
                          (xmlist_result.fail_reason, xmlist_result.output))
            else:
                errmsg = "xm list failed"

            raise errors.HypervisorError(errmsg)

        result = []
        for line in lines:
            # The format of lines is:
            # Name      ID Mem(MiB) VCPUs State  Time(s)
            # Domain-0   0  3418     4 r-----    266.2
            data = line.split()
            if len(data) != 6:
                raise errors.HypervisorError("Can't parse output of xm list,"
                                             " line: %s" % line)
            try:
                data[1] = int(data[1])
                data[2] = int(data[2])
                data[3] = int(data[3])
                data[5] = float(data[5])
            except (TypeError, ValueError), err:
                raise errors.HypervisorError("Can't parse output of xm list,"
                                             " line: %s, error: %s" % (line, err))
            # skip the Domain-0 (optional)
            if include_node or data[0] != 'Domain-0':
                result.append(data)

        return result

    def getInstanceInfo(self, instance_name):
        """Get instance properties.

        @param instance_name: the instance name

        @return: tuple (name, id, memory, vcpus, stat, times)

        """
        xm_list = self._getXMList(instance_name == "Domain-0")
        result = None
        for data in xm_list:
            if data[0] == instance_name:
                result = data
                break
        return result


    def getNodeInfo(self):
        """Return information about the node.

        @return: a dict with the following keys (memory values in MiB):
            - memory_total: the total memory size on the node
            - memory_free: the available memory on the node for instances
            - memory_dom0: the memory used by the node itself, if available
            - nr_cpus: total number of CPUs
            - nr_nodes: in a NUMA system, the number of domains
            - nr_sockets: the number of physical CPU sockets in the node

        """
        # note: in xen 3, memory has changed to total_memory
        result = utilsProcess.RunCmd(["xm", "info"])
        if result.failed:
            logging.error("Can't run 'xm info' (%s): %s", result.fail_reason,
                            result.output)
            return None

        xmoutput = result.stdout.splitlines()
        result = {}
        cores_per_socket = threads_per_core = nr_cpus = None
        for line in xmoutput:
            splitfields = line.split(":", 1)

            if len(splitfields) > 1:
                key = splitfields[0].strip()
                val = splitfields[1].strip()
                if key == 'memory' or key == 'total_memory':
                    result['memory_total'] = int(val)
                elif key == 'free_memory':
                    result['memory_free'] = int(val)
                elif key == 'nr_cpus':
                    nr_cpus = result['cpu_total'] = int(val)
                elif key == 'nr_nodes':
                    result['cpu_nodes'] = int(val)
                elif key == 'cores_per_socket':
                    cores_per_socket = int(val)
                    result['cores_per_socket'] = cores_per_socket
                elif key == 'threads_per_core':
                    threads_per_core = int(val)
                    result['threads_per_core'] = threads_per_core
                elif key == 'cpu_mhz':
                    result['cpu_mhz'] = long(val)
                # how to get MIPS?

        if (cores_per_socket is not None and
              threads_per_core is not None and nr_cpus is not None):
            result['cpu_sockets'] = nr_cpus / (cores_per_socket * threads_per_core)

        dom0_info = self.getInstanceInfo("Domain-0")
        if dom0_info is not None:
            result['memory_dom0'] = dom0_info[2]

        return result

    @classmethod
    def __writeConfigFile(cls, vmName, spicehost, spiceport, memory = 300):
        """ Create a hvm config file.
        """ 
        config = StringIO()

        config.write("#\n# %s\n#\n" % datetime.datetime.now())
        config.write(
            "# this is auto-generated by skylarkhost, please don't edit\n#\n")

        kpath = HV_KERNEL_PATH
        config.write("kernel = '%s'\n" % kpath)
        config.write("builder = 'hvm'\n")
        config.write("memory = %d\n" % memory)
        config.write("device_model = '%s'\n" % HV_DEVICE_MODEL)
        diskimgpath = "%s/%s.img" % (HV_DISK_IMG_PATH, vmName)
        config.write("disk = ['file:%s,ioemu:hda,w']\n" % (diskimgpath))
        config.write("vnc = 1\n")
        config.write("vncviewer = 0\n")
        config.write("serial = 'pty'\n")
        config.write("vcpus = 1\n")

        config.write("name = '%s'\n" % vmName)
        config.write("usbdevice = 'tablet'\n")

        config.write("spice = 1\n")
        config.write("spicehost = '%s'\n" % spicehost)
        config.write("spiceport = %d\n" % spiceport)
        config.write("spice_disable_ticketing = 1\n")
        config.write("spiceagent_mouse = 1\n")

        smIO.RemoveFile("%s/%s.cfg" % (HV_VM_CONFIG_PATH, vmName))

        try:
            smIO.WriteFile("%s/%s.cfg" % (HV_VM_CONFIG_PATH, vmName),
                           data = config.getvalue())
        except EnvironmentError, err:
            raise errors.HypervisorError("Cannot write Xen instance confile"
                                   " file %s/%s: %s" %
                                   (HV_VM_CONFIG_PATH, vmName, err))

        return True


    def createInstance(self, vmName, spicehost, spiceport,
                       memory = 300):
        """Create a VM
        """

        diskimgpath = "%s/%s" % (HV_DISK_IMG_PATH, vmName)
        self.__writeConfigFile(vmName, spicehost, spiceport, memory)

        res = utilsProcess.RunCmd(["xm", "create", "%s/%s.cfg" % 
                                  (HV_VM_CONFIG_PATH, vmName)])
        if res.failed:
            print "xm create fals, reason:%s, extra: %s" % (
                                        res.fail_reason,
                                        res.stderr)
            return None
        
        ins = smObjects.Instance(vmName, spicehost, spiceport)

        return ins


    @staticmethod
    def _runXmRestore(checkpointfile, vmName, spicehost, spiceport):
        """Helper function for L{newInstanceBySnapshot, restoreInstance}
        to run "xm restore".
        Assume checkpointfile is ready
        
        @type checkpointfile: str
        @param: the file name of the checkpoint,
         including the complete path, otherwish the current dir 
        """
        res = utilsProcess.RunCmd(["xm", "restore", checkpointfile])
        
        if res.failed:
            print "xm restore fals, reason:%s, extra: %s" % (
                                        res.fail_reason,
                                        res.stderr)
            return None
        
        ins = smObjects.Instance(vmName, spicehost, spiceport)

        return ins


    def newInstanceBySnapshot(self, vmName, spicehost, spiceport):
        """Create a VM from checkpoint template file
        Use our storage system to parse vmName
        """
        # Have a copy from the checkpoint file template,
        # then restore from the copy?
        ckp = "%s/%s.ckp" % (HV_CKP_TEMPLATE_PATH, vmName)
        ins = self._runXmRestore(ckp, vmName, spicehost, spiceport)
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
        ckp = "%s/%s.ckp" % (HV_DISK_IMG_PATH, vmName)

        # Adjust(modify) the spiceport(host) fields of the ckp file
        xckp = XenCheckpoint()
        if not xckp.init(ckp):
            return None
        options = {XenOptions.SPICEHOST: spicehost,
                   XenOptions.SPICEPORT: str(spiceport)}
        if not xckp.adjustCKPHead(**options):
            return None

        ins = self._runXmRestore(ckp, vmName, spicehost, spiceport)
        return ins

    @staticmethod
    def _runXmShutdownInstance(instanceid):
        """ Helper function for L{shutdownInstance}

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """
        res = utilsProcess.RunCmd(["xm", "shutdown", instanceid])

        if res.failed:
            print "xm shutdown %s failed, reason:%s" % (instanceid,
                                                        res.fail_reason)
            return None
        return res

    def shutdownInstance(self, instanceid):
        """ shutdown the vm instance (instanceid)

        @type instanceid: str
        @param instanceid: the actual name of an instance
        """
        return self._runXmShutdownInstance(instanceid)

    @staticmethod
    def _runXmSave(instanceid, ckpfile):
        """ Helper function for L{saveInstance}

        @type instanceid: str
        @param instanceid: the actual name of an instance
        @type ckpfile: str
        @param ckpfile: the file to save the checkpoint,
        including the complete path, otherwish the current dir 
        """
        res = utilsProcess.RunCmd(["xm", "save", instanceid, ckpfile])

        if res.failed:
            print "xm save %s failed, reason:%s, extra: %s" % (instanceid,
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

        import uuid
        import md5
        instanceid = str(uuid.UUID(bytes = md5.new(instanceid).digest())) 

        return self._runXmSave(instanceid, ckpfile)

    def verify(self):
        """Verify the hypervisor.

        For Xen, this verifies that the xend process is running.

        """
        result = utilsProcess.RunCmd(["xm", "info"])
        if result.failed:
            return "'xm info' failed: %s, %s" % (
                                        result.fail_reason,
                                        result.output)


