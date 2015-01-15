#!/usr/bin/env python
# encoding: utf-8
'''
Created on 10.10.2014

@author: jakob
'''

import sys
import os
from optparse import OptionParser 
from zope.interface import implements
from IVMOptions import IVMOptions
import re

class Cli(object):
    implements(IVMOptions)
    
    __version__ = 0.1
    __updated__ = '2014-10-10'
    
    __parser = None
    __opts = None

    def __init__(self):
        program_name = os.path.basename(sys.argv[0])
        program_version = "v%s" % (self.__version__)
        program_build_date = "%s" % (self.__updated__)

        program_version_string = '%s %s (%s)' % (program_name, program_version, program_build_date)
        program_longdesc = "Create XEN VM" 
        program_license = "Copyright 2014 Jakob Warnow Licensed under the GPL2"
        
        self.__parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        
        self.__parser.add_option("--hostname", 
                                 dest="hostname", 
                                 help="""Set the hostname of the new guest system.  Ideally
                                        this will be fully-qualified since several of the hook
                                        scripts will expect to be able to parse a domain name
                                        out of it for various purposes.\n""", 
                                action='store',
                                metavar="host.example.org")
        self.__parser.add_option("--size", dest="size", help="Set the size of the primary disk image.\n", action='store')
        self.__parser.add_option("--memory", 
                                 dest="memory", 
                                 action="store", 
                                 help="Setup the amount of memory allocated to the new instance.\n",
                                 metavar="size")
        self.__parser.add_option("--yesswap", 
                                 dest="yesswap", 
                                 action="store_true", 
                                 help="""Do not create a swap partition. When this option is
                                        used the system will not have a swap entry added to
                                        its /etc/fstab file either.\n""", 
                                 default=False)
        self.__parser.add_option("--pygrub", 
                                 dest="pygrub", 
                                 action="store_true", 
                                 help="DomU should be booted using pygrub.\n", 
                                 default=False)
        self.__parser.add_option("--dist", dest="dist", action="store", help="Specify the distribution you wish to install.\n")
        self.__parser.add_option("--fs", dest="fs", 
                                 action="store", 
                                 help="""Specify the filesystem type to use for the new guest.
                                        Valid choices are 'ext2', 'ext3', 'ext4', 'reiserfs',
                                        'xfs' or 'btrfs'. (Note: pygrub *DOES NOT* support xfs)\n""")
        self.__parser.add_option("--vifname", dest="vifname", action="store", help="Optionally, set a specific vif name for the new instance.\n")
        self.__parser.add_option("--ip", 
                                 dest="ip", 
                                 action="store", 
                                 help="""Setup the IP address of the machine, multiple IPs are
                                        allowed.  When specifying more than one IP the first
                                        one is setup as the "system" IP, and the additional
                                        ones are added as aliases.\n""",
                                 metavar="123.456.789.ABC")
        self.__parser.add_option("--nameserver", 
                                 dest="nameserver", 
                                 help="""Setup the nameserver of the machine, multiple space
                                        separated nameservers are allowed.
                                        If not provided, Dom0's /etc/resolv.conf will be copied
                                        to guest.\n""", 
                                metavar="123.456.789.ABC 123.456.789.DEF")
        self.__parser.add_option("--gateway", dest="gateway", help="Setup the network gateway for the new instance.\n")
        self.__parser.add_option("--netmask", dest="netmask", help="Setup the netmask for the new instance.\n", metavar="123.456.789.ABC")
        self.__parser.add_option("--lvm", 
                                 dest="lvm", 
                                 help="""Specify the volume group to save images within.
                                        If you do not wish to use LVM specify --dir or --evms.
                                        (These three options are mutually exclusive.)\n""")
        self.__parser.add_option("--mac", 
                                 dest="mac", 
                                 help="""Specify the MAC address to use for a given interface.
                                        This is only valid for the first IP address specified,
                                        or for DHCP usage.  (ie. you can add multiple --ip
                                        flags, but the specific MAC address will only be used
                                        for the first interface.)\n""", 
                                metavar="AA:BB:CC:DD:EE:FF")
        self.__parser.add_option("--force", 
                                 dest="force", 
                                 action="store_true",
                                 help="""Force overwriting existing images. This will remove
                                        existing images or LVM volumes which match those which
                                        are liable to be used by the new invocation.\n""",
                                 default=False)   
        self.__parser.add_option("--verbose", 
                                 dest="verbose", 
                                 action="store_true",
                                 help="""Show useful debugging information.\n""",
                                 default=False)   
        self.__parser.add_option("--mirror", 
                                 dest="mirror", 
                                 help="""Setup the mirror to use when installing via
                                        debootstrap. (Default value: mirror used in
                                        /etc/apt/sources.list or for Debian
                                        "http://http.debian.net/debian/" and for Ubuntu
                                        "http://archive.ubuntu.com/ubuntu/")\n""", 
                                metavar="url")
        self.__parser.add_option("--install-source", 
                                 dest="installsourc", 
                                 help="""Specify the source path to use when installing via
                                        a copy or tarball installation.\n""", 
                                metavar="/path/to/tarball")
        self.__parser.add_option("--install-method", 
                                 dest="installmethod", 
                                 help="""Specify the installation method to use. Valid methods
                                        are:
                    
                                        * debootstrap
                                        * cdebootstrap
                                        * rinse
                                        * rpmstrap (deprecated)
                                        * tar (needs --install-source=tarball.tar)
                                        * copy (needs --install-source=/path/to/copy/from)
                    
                                        (Default value for Debian and Ubuntu: debootstrap)\n""", 
                                metavar="method")
        self.__parser.add_option("--hook-script", 
                                 dest="hookscript", 
                                 help="""Hook Script will be load\n""", 
                                metavar="script_name")
        self.__parser.add_option("--dhcp", 
                                 dest="dhcp", 
                                 action="store_true",
                                 help="""The guest will be configured to fetch its networking
                                        details via DHCP.\n""",
                                 default=False)
    def paser(self):
        (opts, args) = self.__parser.parse_args()
        self.__opts = opts
        mandatories = ['hostname']
        
        for m in mandatories:
            if not opts.__dict__[m]:
                print "mandatory option --%s is missing\n" % (m)
                self.__parser.print_help()
                exit(-1)
                
    def get_hostname(self):
        return self.__opts.hostname
    
    def get_size(self):
        return self.__opts.size
        
    def get_memory(self):
        return self.__opts.memory
        
    def get_yesswap(self):
        return self.__opts.yesswap
        
    def get_pygrub(self):
        return self.__opts.pygrub
        
    def get_dist(self):
        return self.__opts.dist
        
    def get_fs(self):
        return self.__opts.fs
    
    def get_vifname(self):
        return self.__opts.vifname
        
    def get_ip(self):
        return self.__opts.ip
        
    def get_nameserver(self):
        return self.__opts.nameserver
        
    def get_gateway(self):
        return self.__opts.gateway
        
    def get_netmask(self):
        return self.__opts.netmask
        
    def get_lvm(self):
        return self.__opts.lvm
        
    def get_mac(self):
        return self.__opts.mac
    
    def get_force(self):
        return self.__opts.force

    def get_verbose(self):
        return self.__opts.verbose
    
    def get_mirror(self):
        return self.__opts.mirror
    
    def get_installsourc(self):
        return self.__opts.installsourc
    
    def get_installmethod(self):
        return self.__opts.installmethod
    
    def get_hookscript(self):
        return self.__opts.hookscript
    
    def get_dhcp(self):
        return self.__opts.dhcp