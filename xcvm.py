#!/usr/bin/env python
# encoding: utf-8
'''
Created on 19.10.2014

@author: jakob
'''
import Cli, os, re
import subprocess

def clearNewline(clearFile):
    with open(clearFile,'r+') as ipFile:
        tmp = ipFile.readlines()
        ipFile.seek(0)
        ipFile.truncate()
        ipFile.seek(0)
        for l in tmp:
            if not re.match(r'^\s*$', l):
                ipFile.write(l)

if __name__ == '__main__':
    print ""
    
    cli = Cli.Cli()
    cli.paser()
    
    vmconf = "/etc/xen/%s.conf" % (cli.get_hostname())
    if os.path.isfile(vmconf):
        print "Config " + vmconf + " exist!"
        exit(-1)
    
    broadcast = None
    gateway = None
    macaddress = None
    cliOptions = "xen-create-image"
    subnetmask = "255.255.255.0"
    nameserver = "85.31.184.7 8.8.8.8"
    lvm = "VolGroup"
    
    ipfreefile = "/etc/ipfree.txt"
    ipdropfile = "/etc/ipdrop.txt"
    
    print cli.get_dhcp()
    
    if cli.get_dhcp() == False:
        if not os.path.isfile(ipfreefile):
            print "ipfree.txt not found!\n"
            exit(-1)
        else:
            clearNewline(ipfreefile)
            
        if not os.path.isfile(ipdropfile):
            print "ipdrop.txt not found!\n"
            exit(-1)
        else:
            clearNewline(ipdropfile)
    
    if cli.get_hostname() != None:
        cliOptions += " --hostname %s" % (cli.get_hostname())
    else:
        print "--hostname option is missing\n"
        exit(-1)

    if cli.get_size() != None:
        cliOptions += " --size %s" % (cli.get_size())
    else:
        cliOptions += " --size 15Gb"

    if cli.get_memory() != None:
        cliOptions += " --memory %s" % (cli.get_memory())
    else:
        cliOptions += " --memory 1Gb"

    if cli.get_yesswap() == False:
        cliOptions += " --noswap"

    if cli.get_pygrub() == True:
        cliOptions += " --pygrub"
    else:
        cliOptions += " --pygrub"
        #print "--pygrub option is missing\n"
        #exit(-1)

    if cli.get_dist() != None:
        cliOptions += " --dist %s" % (cli.get_dist())
    else:
        cliOptions += " --dist wheezy"

    if cli.get_fs() != None:
        cliOptions += " --fs %s" % (cli.get_fs())
    else:
        cliOptions += " --fs ext4"

    if cli.get_vifname() != None:
        cliOptions += " --vifname %s" % (cli.get_vifname())
    else:
        cliOptions += " --vifname %s" % (cli.get_hostname())

    if cli.get_ip() != None:
        cliOptions += " --ip %s" % (cli.get_ip())
    elif cli.get_dhcp() == True:
        cliOptions += " --dhcp"
    else:

        rIpFree = open(ipfreefile, 'r')

        if os.stat(ipfreefile).st_size == 0:
            print "No ip`s found, maybe ip are emty?!\n"
            exit(-1)

        lines = rIpFree.readline()
        rIpFree.close()
        (ip, mac) = lines.split(";")
        cliOptions += " --ip %s" % (ip)
        macaddress = mac[:-1]
        ipTmp = ip.split(".")
        gateway = "%s.%s.%s.1" % (ipTmp[0],ipTmp[1],ipTmp[2])
        broadcast = "%s.%s.%s.255" % (ipTmp[0],ipTmp[1],ipTmp[2])
        cliOptions += " --broadcast %s" % (broadcast)

    if cli.get_nameserver() != None:
        cliOptions += " --nameserver %s" % (cli.get_nameserver())
    elif cli.get_dhcp() == True:
        pass
    else:
        cliOptions += " --nameserver %s" % (nameserver)

    if cli.get_gateway() != None:
        cliOptions += " --gateway %s" % (cli.get_gateway())
    elif cli.get_dhcp() == True:
        pass
    else:
        cliOptions += " --gateway %s" % (gateway)

    if cli.get_netmask() != None:
        cliOptions += " --netmask %s" % (cli.get_netmask())
    elif cli.get_dhcp() == True:
        pass
    else:
        cliOptions += " --netmask %s" % (subnetmask)

    if cli.get_lvm() != None:
        cliOptions += " --lvm %s" % (cli.get_lvm())
    else:
        cliOptions += " --lvm %s" % (lvm)

    if cli.get_mac() != None:
        cliOptions += " --mac %s" % (cli.get_mac())
    else:
        cliOptions += " --mac %s" % (macaddress)
        
    if cli.get_force() == True:
        cliOptions += " --force"
        
    if cli.get_verbose() == True:
        cliOptions += " --verbose"
        
    if cli.get_mirror() != None:
        cliOptions += " --mirror %s" % (cli.get_mirror())
        
    if cli.get_installsourc() != None:
        cliOptions += " --install-source %s" % (cli.get_installsourc())
        
    if cli.get_installmethod() != None:
        cliOptions += " --install-method %s" % (cli.get_installmethod())
        
    if cli.get_hookscript() != None:
        if not os.path.exists("/usr/lib/xen-tools/hookscripts"):
            print "Hook Script-Folder dont exist."
            exit(-1)
        if not os.path.exists("/usr/lib/xen-tools/hookscripts/" + cli.get_hookscript()):
            print "Hook Script dont exist."
            exit(-1)
        cliHookScript = "cp /usr/lib/xen-tools/hookscripts/%s /usr/lib/xen-tools/debian.d/97-%s.cfg" % (cli.get_hookscript(), cli.get_hookscript())
        p = subprocess.Popen(cliHookScript, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while(True):
            retcode = p.poll() #returns None while subprocess is running
            line = p.stdout.readline()
            print line[:-1]
            if(retcode is not None):
                break
    

    p = subprocess.Popen(cliOptions, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    while(True):
        retcode = p.poll() #returns None while subprocess is running
        line = p.stdout.readline()
        print line[:-1]
        if(retcode is not None):
            break
        
    if cli.get_dhcp() == False:
        vmconf = "/etc/xen/%s.cfg" % (cli.get_hostname())
        if os.path.isfile(vmconf):
            rIpFree = open(ipfreefile, 'r')
            lines = rIpFree.readlines()
            rIpFree.close()
            with open(ipdropfile, "a") as aIpDrop:
                aIpDrop.write(lines[0])
            del lines[0]
            wIpFree = open(ipfreefile, 'w')
            wIpFree.writelines(lines)
            wIpFree.close()
            clearNewline(ipfreefile)
            clearNewline(ipdropfile)        
    
    if cli.get_hookscript() != None:
        cliHookScript = "/usr/lib/xen-tools/debian.d/97-%s.cfg" % (cli.get_hookscript())
        if os.path.exists(cliHookScript):
            p = subprocess.Popen("rm " + cliHookScript, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            while(True):
                retcode = p.poll() #returns None while subprocess is running
                line = p.stdout.readline()
                print line[:-1]
                if(retcode is not None):
                    break