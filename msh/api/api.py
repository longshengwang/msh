# -*- coding:utf8 -*-
from msh.service.db.dbService import DBService
from msh.service.output.pexpectInput import PexpectClient
from msh.constants.PasswordErrorException import PasswordErrorException
import time

from msh.service.color import UseStyle, redStr, greenStr

class Api:

    def __init__(self):
        self.db = DBService()
        self.pexpClient = PexpectClient()

    def add_ssh_connect(self, host, user, password, port=22, alias=''):
        self.db.put_ssh_key(user, password, host, port, alias, time.time())

    def del_ssh_connect(self, host):
        self.db.delete_ssh_key(host)

    def update_ssh_connect(self, host, user, name):
        self.db.update_ssh_key(host, user, name)

    def list_ssh_connects(self):
        return self.db.get_all_ssh_list()

    def list_connects_order_by_time(self):
        return self.db.get_all_ssh_list('timestamp')

    def get_ssh_connect(self, host):
        res = self.db.get_ssh_key(host)
        # print res
        return res
        # return self.db.get_ssh_key(host)

    def login(self, host, user = None, password = None, port = 22):
        if user is not None and password is not None:
            self.pexpClient.set_param(host, user, password, port)
            self.pexpClient.connect()
            try:
                import sys
                sys.stdout.write(UseStyle("Try to login %s@%s \n"%(user, host), mode = 'bold',fore='green'))
                # sys.stdout.write(UseStyle("**********************************\n", mode = 'bold',fore='cyan'))
                # sys.stdout.write(UseStyle("*     __  __   ____    _   _     *\n", mode = 'bold',fore='cyan'))
                # sys.stdout.write(UseStyle("*    |  \/  | / ___|  | | | |    *\n", mode = 'bold',fore='cyan'))
                # sys.stdout.write(UseStyle("*    | |\/| | \___ \  | |_| |    *\n", mode = 'bold',fore='cyan'))
                # sys.stdout.write(UseStyle("*    | |  | |  ___) | |  _  |    *\n", mode = 'bold',fore='cyan'))
                # sys.stdout.write(UseStyle("*    |_|  |_| |____/  |_| |_|    *\n", mode = 'bold',fore='cyan'))
                # sys.stdout.write(UseStyle("*                                *\n", mode='bold', fore='cyan'))
                # sys.stdout.write(UseStyle("**********************************\n", mode='bold', fore='cyan'))

                self.pexpClient.login()
                self.pexpClient.interact()
            except PasswordErrorException,e:
                print redStr("Password error, please make sure the correctness of password!")
                raise
        else:
            res = self.get_ssh_connect(host)
            self.login(host, res.get('name'),res.get('passwd'), res.get('port'))

    def login_fuzzy(self, key):
        ssh_cons = self.list_ssh_connects()
        # hosts = [con.get('host') for con in ssh_cons]
        ssh_con_choose = []
        for con in ssh_cons:
            host = con.get('host')
            params = host.split('.')
            if params.count(key) > 0:
                ssh_con_choose.append(con)
            else:
                if con.get('alias').find(key) != -1:
                    ssh_con_choose.append(con)

        return ssh_con_choose

