# -*- coding:utf8 -*-

databases = ['Security', 'SSHList']

Security_db_create_sql = '''CREATE TABLE Security(key TEXT NOT NULL) ;'''
SSHList_db_create_sql = '''
  CREATE TABLE SSHList (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,passwd TEXT,host CHAR(50) NOT NULL,port INTEGER, alias TEXT,timestamp INTEGER NOT NULL);
  '''

#     conn.execute(''' ''')
# (id, name, passwd, host, timestamp)
db_create_sql_list = {
                  'Security': Security_db_create_sql,
                  'SSHList': SSHList_db_create_sql
                }


SSHSchedule = {
    "yes": 1,
    "password":2,
    "other":3,
}