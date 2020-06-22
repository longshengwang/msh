# -*- coding:utf-8 -*-
import sqlite3

'''
db file: ssh.db

    table name: SSHList
    column:
           (id, name, passwd, host, timestamp)
    trigger:
           keep the count of db is 1000

    table name: Security
    column:
           (passwd)
    trigger:
           keep the count of db is 1
'''
from msh.constants.Constants import databases, db_create_sql_list
import os
from os.path import expanduser



class DBService:
    def __init__(self):
        self.conn = None
        self.connect()
        # self.dbs = ['Security', 'SSHList']

    def connect(self):
        home = expanduser("~")
        if not os.path.exists(home + '/.msh'):
            os.mkdir(home + '/.msh')
        db_path = home + '/.msh/ssh.db'
        self.conn = sqlite3.connect(db_path)
        self._check_dbs()

    def _check_dbs(self):
        for db_name in databases:
            db_exist = self._db_exist(db_name)
            if db_exist == 0:
                self._create_db(db_create_sql_list.get(db_name))

    def _db_exist(self, db_name):
        cursor = self.conn.execute(
            'select count(*)  from sqlite_master where type=\'table\' and name = \'%s\';' % db_name)
        res = cursor.fetchone()
        return res[0]

    def _create_db(self, sql):
        self.conn.execute(sql)

    def _del_db(self, db_name):
        self.conn.execute('drop table %s' % db_name)

    def get_security_key(self):
        cursor = self.conn.execute('select key from Security')
        row = cursor.fetchone()
        return row[0]

    def put_security_key(self, key):
        self.conn.execute("DELETE from Security")
        self.conn.execute("INSERT INTO Security (key) VALUES ('%s')" % key);
        self.conn.commit()

    def get_all_ssh_list(self, order_by='id'):
        # self.conn.text_factory = str
        cursor = self.conn.execute(
            "SELECT id,name,passwd,host,port, alias, timestamp from SSHList order by %s desc limit 100" % order_by)
        ssh_list = []
        for row in cursor:
            ssh_list.append({
                'id': row[0],
                'name': row[1],
                'passwd': row[2],
                'host': row[3],
                'port': row[4],
                'alias': row[5],
                'timestamp': row[6]});

        # ssh_list = list(reversed(ssh_list))
        return ssh_list

    def put_ssh_key(self, name, passwd, host, port, alias, timestamp):
        sql = "INSERT INTO SSHList (id, name, passwd, host, port, alias, timestamp) \
              VALUES (null,'%s','%s','%s', %d, '%s', %d)" % (name, passwd, host, port, alias, timestamp)
        self.conn.execute(sql)
        self.conn.commit()

    def delete_ssh_key(self, host):
        self.conn.execute('DELETE FROM SSHList WHERE host=\'%s\'' % host)
        self.conn.commit()

    def update_ssh_key(self, host, username, password):
        sql = 'UPDATE SSHLIST SET name=\'%s\' , passwd=\'%s\' WHERE host=\'%s\'' % (username, password, host)
        self.conn.execute(sql)
        self.conn.commit()

    def get_ssh_key(self, host):
        sql = 'SELECT id,name,passwd,host,port, timestamp from SSHList WHERE host = \'%s\'' % host
        cursor = self.conn.execute(sql)
        # cursor = self.conn.execute('SELECT id,name,passwd,host,timestamp from SSHList WHERE host = \'%s\''%host)
        row = cursor.fetchone()
        if row is not None:
            return {'id': row[0], 'name': row[1], 'passwd': row[2], 'host': row[3],'port': row[4], 'timestamp': row[5]}
        else:
            return None

    def __del__(self):
        # print '[log] leave db service'
        self.conn.close()


if __name__ == "__main__":
    db = DBService()
    # db._del_db('Security')
    # db.put_security_key('woshi')
    # print db.get_security_key()
    # import time
    # db.put_ssh_key('root','123456','192.168.205.22',time.time())
    for i in db.get_all_ssh_list():
        print i
    # print db.get_security_key()

    # conn = sqlite3.connect('/Users/wls/.msh/ssh.db')
    # cur = conn.execute('SELECT id,name,passwd,host,timestamp FROM SSHList WHERE host = \'20.0.0.130\'')
    # for xx in cur:
    #     print xx
    '''
    conn = sqlite3.connect('cmd.db')

    cur = conn.execute('select *  from sqlite_master')
    # cur = conn.execute('drop table CurCmd;')
    # cur = conn.execute('drop table xx;')
    print cur.fetchone()
    # for xx in cur:
    #     print xx
    '''

    #
# conn.execute("DELETE from CMD")
#     conn.execute("DELETE from CurCmd")
#     conn.commit()
#     conn.close()

#     conn.execute("INSERT INTO CMD (id,cmd,timestamp,ip) \
#       VALUES (null,'123',1241,'asdgasdg');")
#     conn.commit()
#     for x in conn.execute("select count() from CMD;"):
#         print x[0]
#     conn.execute('drop table CMD')
#
#     conn.execute('''CREATE TABLE CurCmd
#             (cmd           TEXT    NOT NULL,
#             timestamp            INT     NOT NULL,
#             ip        CHAR(50) NOT NULL) ; ''')
#
#     conn.execute('''CREATE TABLE CMD
#             (id INTEGER PRIMARY KEY AUTOINCREMENT,
#             cmd           TEXT    NOT NULL,
#             timestamp            INTEGER     NOT NULL,
#             ip        CHAR(50) NOT NULL) ; ''')

#     db = DBService()
#     db.connect()

#     db.put(Cmd('cat12313 a12a',1231421,'1.0.0.2'))
#
#     db.put(Cmd('cat12313 a12a',1231421,'1.0.0.13'))

#     print db._get_cur_cmd()
#
#     db.get()
#
#     print db._get_cur_cmd()
#     allcmd = db.getall()
#     print allcmd
