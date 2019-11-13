# -*- coding:utf8 -*-
# from __future__ import print_function
import os
import ipaddress
import sys
import getpass
from msh.service.color import redStr, greenStr


class InputClient:

    def __init__(self):
        pass

    def input_host(self):
        host = raw_input("Host:")
        # ipaddress.
        while not is_ip(host):
            sys.stdout.write(redStr("Ip format is not correct！\n"))
            host = raw_input("Host:")
        return host

    def input_username(self):
        name = raw_input("User:")
        return name

    def input_password(self):
        p = getpass.getpass('input your password:')
        return p
        # getpass.getpass()


def is_ip(address):
    try:
        address = unicode(address)
        ipaddress.ip_address(address)
        return True
    except Exception,e:
        return False


def is_host_can_connect(host):
    if (os.system('ping -c 1 -W 1000 %s > /dev/null'%host) == 0):
        return True
    else:
        return False

'''
# ip = IPy.IP('10.0.0.110')
# print ip.get_mac()
a = "1.0.0.1"
b = unicode(a)
ipa = ipaddress.ip_address(a)
print(ipa)
'''
# print is_host_can_connect("20.0.0.10")
# if(os.system('ping -c 1 -W 100 20.0.0.30 > /dev/null')==0):
#   print 'OK'
# else:
#   print 'Connection failed'
#
# t = InputClient()
# pas = t.input_password()
# print pas