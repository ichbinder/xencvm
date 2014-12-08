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
                                        out of it for various purposes.""", 
                                action='store',
                                metavar="host.example.org")
        self.__parser.add_option("--size", dest="size", help="Set the size of the primary disk image.", action='store')
        self.__parser.add_option("--memory", 
                                 dest="memory", 
                                 action="store", 
                                 help="Setup the amount of memory allocated to the new instance.",
                                 metavar="size")
        self.__parser.add_option("--yesswap", 
                                 dest="yesswap", 
                                 action="store_true", 
                                 help="""Do not create a swap partition. When this option is
                                        used the system will not have a swap entry added to
                                        its /etc/fstab file either.""", 
                                 default=False)
        self.__parser.add_option("--pygrub", 
                                 dest="pygrub", 
                                 action="store_true", 
                                 help="DomU should be booted using pygrub.", 
                                 default=False)
        self.__parser.add_option("--dist", dest="dist", action="store", help="Specify the distribution you wish to install.")
        self.__parser.add_option("--fs", dest="fs", 
                                 action="store", 
                                 help="""Specify the filesystem type to use for the new guest.
                                        Valid choices are 'ext2', 'ext3', 'ext4', 'reiserfs',
                                        'xfs' or 'btrfs'. (Note: pygrub *DOES NOT* support xfs)""")
        self.__parser.add_option("--vifname", dest="vifname", action="store", help="Optionally, set a specific vif name for the new instance.")
        self.__parser.add_option("--ip", 
                                 dest="ip", 
                                 action="store", 
                                 help="""Setup the IP address of the machine, multiple IPs are
                                        allowed.  When specifying more than one IP the first
                                        one is setup as the "system" IP, and the additional
                                        ones are added as aliases.""",
                                 metavar="123.456.789.ABC")
        self.__parser.add_option("--nameserver", 
                                 dest="nameserver", 
                                 help="""Setup the nameserver of the machine, multiple space
                                        separated nameservers are allowed.
                                        If not provided, Dom0's /etc/resolv.conf will be copied
                                        to guest.""", 
                                metavar="123.456.789.ABC 123.456.789.DEF")
        self.__parser.add_option("--gateway", dest="gateway", help="Setup the network gateway for the new instance.")
        self.__parser.add_option("--netmask", dest="netmask", help="Setup the netmask for the new instance.", metavar="123.456.789.ABC")
        self.__parser.add_option("--lvm", 
                                 dest="lvm", 
                                 help="""Specify the volume group to save images within.
                                        If you do not wish to use LVM specify --dir or --evms.
                                        (These three options are mutually exclusive.)""")
        self.__parser.add_option("--mac", 
                                 dest="mac", 
                                 help="""Specify the MAC address to use for a given interface.
                                        This is only valid for the first IP address specified,
                                        or for DHCP usage.  (ie. you can add multiple --ip
                                        flags, but the specific MAC address will only be used
                                        for the first interface.)""", 
                                metavar="AA:BB:CC:DD:EE:FF")
        self.__parser.add_option("--force", 
                                 dest="force", 
                                 help="""Force overwriting existing images. This will remove
                                        existing images or LVM volumes which match those which
                                        are liable to be used by the new invocation.""")   
        self.__parser.add_option("--verbose", 
                                 dest="verbose", 
                                 help="""Show useful debugging information.""")           
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