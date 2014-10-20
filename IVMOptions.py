'''
Created on 18.10.2014

@author: jakob
'''

from zope.interface import Interface

class IVMOptions(Interface):
    
    def get_hostname(self):
        """hostname"""
    
    def get_size(self):
        """size"""
        
    def get_memory(self):
        """memory"""
        
    def get_yesswap(self):
        """noswap"""
        
    def get_pygrub(self):
        """pygrub"""
        
    def get_dist(self):
        """dist"""
        
    def get_fs(self):
        """fs"""
    
    def get_vifname(self):
        """vifname"""
        
    def get_ip(self):
        """ip"""
        
    def get_nameserver(self):
        """nameserver"""
        
    def get_gateway(self):
        """gateway"""
        
    def get_netmask(self):
        """netmask"""
        
    def get_lvm(self):
        """lvm"""
        
    def get_mac(self):
        """mac"""


        