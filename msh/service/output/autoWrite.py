# -*- coding:utf8 -*-
'''
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
# m = PyMouse()
k = PyKeyboard()
k.type_string('ssh root@10.0.0.4')

k.press_key('Return')
time.sleep(0.5)
# print 'xxxxxx'
k.type_string('123456')
k.press_key('Return')
'''
import pexpect
import sys

if __name__ == '__main__':
    user = 'root'
    ip = '20.0.0.130'
    # ip = '92.0.0.13'
    mypassword = '123456'

    print user
    child = pexpect.spawn('ssh %s@%s' % (user, ip))
    # child.logfile = sys.stdout
    # print child.before
    child.expect('yes|password|#')
    print child.after
    import time
    # time.sleep(2)
    # child.close()
    # pass
    # print '-----'
    #
    # print '-----'
    # child.sendline('yes')
    # x = child.expect('password:')
    # print '======'
    # print x
    # print child.before
    # print '======'
    # # print child.before
    child.sendline(mypassword)
    child.expect('#')
    # # x = child.sendline('ls -la')
    # child.expect('#')
    #
    # # print child.before
    # # child.expect(':')
    # # child.sendline(mypassword)
    # # child.expect('#')
    # # child.sendline('ls -la')
    # # child.expect('#')
    # # print child.before  # Print the result of the ls command.
    # # child.sendline("echo '112' >> /home/forever/1.txt ")
    child.interact()  # Give control of the child to the user.
    # pass

