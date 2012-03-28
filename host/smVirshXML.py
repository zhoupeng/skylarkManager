#!/usr/bin/env python
#
# Filename: host/smVirshXML.py
#
# -------------------------------------------------------------------
#
# Author:
#  Zhou Peng <ailvpeng25@gmail.com>, 2011.11 ~
#
# -------------------------------------------------------------------
import libconf
import os
from xml.etree.ElementTree import ElementTree
import sys
from cStringIO import StringIO
import datetime

class VirshOptions:
    """represent libvirt virsh vm xml element or attribute
    """
    # The key name of optinos to be modified
    SPICEPORT = "devices/graphics[@port]"
    SPICEHOST = "devices/graphics[@listen]"
    AGENTMOUSE = "devices/graphics/mouse"
    FSTYPE = "devices/filesystem[@type]"
    FSACCESSMODE = "devices/filesystem[@accessmode]"
    FSDRTYPE = "devices/filesystem/driver[@type]"
    FSDRWRPOLOCY = "devices/filesystem/driver[@wrpolicy]"
    FSSOURCEDIR = "devices/filesystem/source[@dir]"
    FSTARGETDIR = "devices/filesystem/target[@dir]"

    # The paths of related elements or attributes
    GRAPHICS = "devices/graphics"
    LISTEN = "devices/graphics/listen" # [@address]
    GRAPHICSTYPE = "devices/graphics[@type]" # Not used yet
    FILESYSTEM = "devices/filesystem"
    FSDRIVER = "devices/filesystem/driver"
    FSSOURCE = "devices/filesystem/source"
    FSTARGET = "devices/filesystem/target"

class VirshVMXML:
    """ helper for virsh vm xml modifying
    """
    def __init__(self):
        # str, the xml file name(including the complete path)
        self._xmlfile = None
        # ElementTree object of xml file
        self._tree = None

    def init(self, xml):
        """ construct self._tree object from xml file

        @type xml: str
        @param xml: the virsh vm xml file,
        including the complete path, otherwish the current dir

        @rtype: int
        @return: 1 if success, else 0 
        """
        if not os.path.exists(xml):
            return 0

        self._xmlfile = xml
        self._tree = ElementTree()
        self._tree.parse(xml)

        return 1

    def find(self, path):
        """ find to check if the sub element exists, if exist
        return the Element type elem, else return None.

        @type path: str
        @param path: the path of the sub element 
        """
        return self._tree.find(path)

    def adjust(self, **options):
        """ modify the vm's xml config file based on options

        @type options: dir, keyward arg
        @param options: like {SPICEHOST: 'xxx',
                              SPICEPORT: xxx(str)}
        @rtype: int
        @return: 1 if success, else 0
        """
        if not self._tree:
            print "init first"
            return 0

        tag = 0 # tag if modified
        for k in options.keys():
            if k == VirshOptions.SPICEHOST:
                graphics = self._tree.find(VirshOptions.GRAPHICS)
                """FutureWarning: The behavior of this method will change
                in future versions.
                Use specific 'len(elem)' or 'elem is not None' test instead.
                if not graphics:
                By Python 2.7.2 (default, Oct 27 2011, 01:40:22)"""
                #if not graphics:
                if graphics is None:
                    return 0
                graphics.attrib["listen"] = options[k]
                listen = graphics.find("listen")
                """Inconceivable that "if listen:" is false
                when listen is not None"""
                #if listen:
                #    listen.attrib["address"] = options[k]
                #listen.attrib["address"] = options[k]
                if listen is not None:
                    listen.attrib["address"] = options[k]

                tag = 1
            if k == VirshOptions.SPICEPORT:
                graphics = self._tree.find(VirshOptions.GRAPHICS)
                if graphics is None:
                    return 0
                graphics.attrib["port"] = options[k]

                tag = 1
            if k == VirshOptions.AGENTMOUSE:
                agentmouse = self._tree.find(VirshOptions.AGENTMOUSE)
                # if no agent mouse sub-elem, ignore this setting
                if agentmouse is None:
                    continue
                agentmouse.attrib["mode"] = options[k]

                tag = 1
            if k == VirshOptions.FSSOURCEDIR:
                fssource = self._tree.find(VirshOptions.FSSOURCE)
                if fssource is not None:
                    fssource.attrib["dir"] = options[k]
                    tag = 1
            if k == VirshOptions.FSTARGETDIR:
                fstarget = self._tree.find(VirshOptions.FSTARGET)
                if fstarget is not None:
                    fstarget.attrib["dir"] = options[k]
                    tag = 1
            if k == VirshOptions.FSDRTYPE:
                fsdriver = self._tree.find(VirshOptions.FSDRIVER)
                if fsdriver is not None:
                    fsdriver.attrib["type"] = options[k]
                    tag = 1
            if k == VirshOptions.FSDRWRPOLOCY:
                fsdriver = self._tree.find(VirshOptions.FSDRIVER)
                if fsdriver is not None:
                    fsdriver.attrib["wrpolicy"] = options[k]
                    tag = 1
            if k == VirshOptions.FSTYPE:
                fs = self._tree.find(VirshOptions.FILESYSTEM)
                if fs is not None:
                    fs.attrib["type"] = options[k]
                    tag = 1
            if k == VirshOptions.FSACCESSMODE:
                fs = self._tree.find(VirshOptions.FILESYSTEM)
                if fs is not None:
                    fs.attrib["accessmode"] = options[k]
                    tag = 1

        if tag:
            sio = StringIO()
            sio.write("<!--\n")
            sio.write("Modified at %s\n" % datetime.datetime.now())
            sio.write("This is auto-generated by "
                      "skylarkhost, please don't edit.\n")
            sio.write("-->\n")
            #self._tree.write(self._xmlfile)
            self._tree.write(sio)
            try:
                f = open(self._xmlfile, 'w')
                f.write(sio.getvalue())
                f.close()
            except IOError, err:
                print err
                f.close()
                return 0

        return 1
