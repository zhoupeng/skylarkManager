#!/usr/bin/env python
#
# Filename: host/smXen.py
#
# -------------------------------------------------------------------
#
# 
#
# -------------------------------------------------------------------
import smProcess as utilsProcess
import smRetry as utilsRetry

class XenNode(object):

    def getMemInfo(self):
        pass

    def getCPUInfo(self):
        pass

    @staticmethod
    def _runXmList(xmlist_errors):
        """Helper function for L{_GetXMList} to run "xm list".

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
        xm_list = self._getXMList(instance_name=="Domain-0")
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
                elif key == 'threads_per_core':
                    threads_per_core = int(val)

        if (cores_per_socket is not None and
              threads_per_core is not None and nr_cpus is not None):
            result['cpu_sockets'] = nr_cpus / (cores_per_socket * threads_per_core)

        dom0_info = self.getInstanceInfo("Domain-0")
        if dom0_info is not None:
            result['memory_dom0'] = dom0_info[2]

        return result

    def verify(self):
        """Verify the hypervisor.

        For Xen, this verifies that the xend process is running.

        """
        result = utilsProcess.RunCmd(["xm", "info"])
        if result.failed:
            return "'xm info' failed: %s, %s" % (result.fail_reason, result.output)

