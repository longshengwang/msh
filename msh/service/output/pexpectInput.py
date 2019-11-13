# -*- coding:utf8 -*-


import pexpect
import sys
from msh.constants.Constants import SSHSchedule
from msh.constants.PasswordErrorException import PasswordErrorException
import signal

import struct, fcntl, termios
PASSWORD = "password"
YES = "yes"


class PexpectClient:

    def __init__(self, host = None, username = None, password = None):
        self.host = host
        self.username = username
        self.password = password
        self.child = None

    def set_param(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        ssh_str = 'ssh %s@%s'%(self.username, self.host)
        if self.port != 22:
            ssh_str = 'ssh -p %s %s@%s' % (str(self.port), self.username, self.host)

        self.child = pexpect.spawn(ssh_str)
        # self.child = pexpect.spawn('ssh %s@%s'%(self.username, self.host))

    def check_ssh_process(self):
        self.child.expect('password:|Password:|PASSWORD:|yes|[#\$]')
        cafter = self.child.after
        # print cafter
        if cafter == "yes":
            return SSHSchedule.get('yes')
        elif cafter == "password:" or cafter == "Password:" or cafter == "PASSWORD:":
            return SSHSchedule.get("password")
        else:
            return SSHSchedule.get("other")

    def login(self):
        status = self.check_ssh_process()
        if status == SSHSchedule.get("yes"):
            # print "Login with yes"
            self.login_with_yes()
        elif status == SSHSchedule.get("password"):
            # print "Login with password"
            self.login_with_password()
        else:
            sys.stdout.write(self.child.before + self.child.after)

    def login_with_yes(self):
        self.child.sendline(YES)
        self.child.expect(PASSWORD)
        self.login_with_password()

    def login_with_password(self):
        if self.password is None:
            return
        self.child.sendline(self.password)
        self.child.expect("Permission denied|Password:|password:|[#\$]|\s")
        if self.child.after == "Permission denied" or self.child.after == "Password:" or self.child.after == "password:" :
            raise PasswordErrorException
        else:
            sys.stdout.write(self.child.before + self.child.after)
            # sys.stdout.write(self.child.after)

    def interact(self):
        # print self.child.getwinsize()

        s = struct.pack("HHHH", 0, 0, 0, 0)
        a = struct.unpack('HHHH', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
        self.child.setwinsize(a[0], a[1])
        signal.signal(signal.SIGWINCH, self.sigwinch_passthrough)
        self.child.interact()

    def close(self):
        self.child.close()

    def sigwinch_passthrough(self, sig, data):
        # Check for buggy platforms (see pexpect.setwinsize()).
        # if 'TIOCGWINSZ' in dir(termios):
        #     TIOCGWINSZ = termios.TIOCGWINSZ
        # else:
        #     TIOCGWINSZ = 1074295912  # assume
        s = struct.pack("HHHH", 0, 0, 0, 0)
        a = struct.unpack('HHHH', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
        self.child.setwinsize(a[0], a[1])

    def __del__(self):
        pass
