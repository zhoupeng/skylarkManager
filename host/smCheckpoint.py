#!/usr/bin/env python
#
# Filename: host/smCheckpoint.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.10 ~
#
# -------------------------------------------------------------------
import libconf

import smSXP as sxp
import struct
import os
from StringIO import StringIO

class XenOptions(object):
    """ represent xen cfg options's name
    """

    SPICEPORT = "spiceport"
    SPICEHOST = "spicehost"

class XenCheckpoint(object):
    """ helper for checkpoint
    """

    H_SIGNATURE = 'LinuxGuestRecord'

    def __init__(self): 
        self._h_prefix = XenCheckpoint.H_SIGNATURE # str
        self._h_size = None # 4B binanry str, size of cfg
        self._h_size_val = 0 # the int value of ._h_size
		# str, the cfg part of head, s-expression represented by str
        self._h_head_cfg = None # cfg part
        self._header = None # str, the whole head
		# str, the checkpoint file name(including the complete path)
        self._ckpfile = None

    def init(self, ckpfile):
        """ read the whole header of checkpoint and init the filds

        @type ckpfile: str
        @param ckpfile: the checkpoint file,
        including the complete path, otherwish the current dir

        @rtype: int
        @return: 1 if success, else 0 
        """
        if not ckpfile:
            return 0

        self._ckpfile = ckpfile

        try:
            f = open(ckpfile, 'rb')

            pre = f.read(len(XenCheckpoint.H_SIGNATURE))
            if pre != XenCheckpoint.H_SIGNATURE:
                print "unknown prefix: %s" % pre
                self._ckpfile = None
                return 0
            self._h_prefix = pre

            self._h_size = f.read(4)
            
            # '>' big-endian, It's necessary here.
            # '!' network(=big-endian)
            self._h_size_val = struct.unpack('!i', self._h_size)[0]

            self._h_head_cfg = f.read(self._h_size_val)

            self._header = self._h_prefix + self._h_size + self._h_head_cfg

        except (IOError, struct.error), err:
            print err
            self._ckpfile = None
            f.close()
            return 0

        f.close()
        return 1

    def _modifyCKPHeadStr(self, options):
        """ modify exp self._h_head_cfg based on options

        @type options: dir
        @param options: like {'spicehost': 'xxx',
                              'spiceport': xxx(str)}
		@rtype: str
		@return: 1 success, else 0
        """
        str_io = StringIO(self._h_head_cfg)
        sxp_obj = sxp.parse(str_io)
        sxp_obj = sxp_obj[0]
        str_io.close()

        # python param and return use reference for list,
        # which makes the modify reflecting to sxp_obj
        for k in options.keys():
            if k == XenOptions.SPICEPORT:
                cld_spiceport = sxp.child_with_element(sxp_obj,
                                              XenOptions.SPICEPORT)
                ## FIXME: how to deal with if it's <
                #if len(cld_spiceport[1]) > len(options[k]):
                #    options[k] = (len(cld_spiceport[1]) -
                #                len(options[k])) * '0' + options[k]
                cld_spiceport[1] = options[k]
            elif k == XenOptions.SPICEHOST:
                cld_spicehost = sxp.child_with_element(sxp_obj,
                                              XenOptions.SPICEHOST)

                ## FIXME: how to deal with if it's <
                #if len(cld_spicehost[1]) > len(options[k]):
                #    options[k] = (len(cld_spicehost[1]) -
                #                len(options[k])) * '0' + options[k]
                cld_spicehost[1] = options[k]
            else:
                print "Untion option: %s" % k
                return 0

        th = self._h_head_cfg
        self._h_head_cfg = sxp.to_string(sxp_obj)
        # fill ' ' as placeholder, not '\0', '\0' cause sxp parse err
        if len(th) > len(self._h_head_cfg):
            self._h_head_cfg = (self._h_head_cfg +
                                (len(th) - len(self._h_head_cfg)) * ' ')
                               
        # sync with ._h_head_cfg
        self._header = self._header.replace(th, self._h_head_cfg, 1)
        return 1

    def _overrideCKPHead(self):
        """ override ckpfile's header with _h_head_cfg, sync to disk

		@rtype: int
		@return: 1 success, else 0
        """
        try:
            f = open(self._ckpfile, 'rb+')
            f.seek(0)
            f.write(self._header)

            # two lines below ensure to write file's data to disk
            f.flush()
            os.fsync(f.fileno())

            f.close()
            return 1
        except IOError, err:
            print err
            f.close()
            return 0

    def adjustCKPHead(self, **options):
        """ modify the checkpoint file's header based on options

        @type options: dir, keyward arg
        @param options: like {'spicehost': 'xxx',
                              'spiceport': xxx(str)}
        @rtype: int
        @return: 1 if success, else 0
        """
        if not self._ckpfile:
            print "init first"
            return 0

        if not self._modifyCKPHeadStr(options):
            return 0

        return self._overrideCKPHead()

    def geth_prefix(self):
        return self._h_prefix

    def geth_size(self):
        return self._h_size

    def geth_size_val(self):
        return self._h_size_val

    def geth_head_cfg(self):
        return self._h_head_cfg 

    def getheader(self):
        return self._header

    def getckpfile(self):
        return self._ckpfile

