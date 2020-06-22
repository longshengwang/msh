# -*- coding:utf8 -*-
import getpass
import sys
from optparse import OptionParser

from pexpect.exceptions import TIMEOUT

from api.api import Api
from api.inputClient import InputClient
from api.outputClient import OutputClient
from constants.ParamsException import ParamsException
from service.color import redStr, greenStr


def main():
    inputClient = InputClient()
    api = Api()
    usage = "usage: %prog [options] [arg]"
    parser = OptionParser(usage)
    parser.add_option('-l', '--list', action='store_true', dest="iflist", help=u"list all ssh information")
    parser.add_option('-a', '--add', action='store', dest="ifadd",
                      help=u"Add ssh information.<name>@<ip>[:<ssh port>][@<alias>]. Example: root:1.1.1.1:1010-home1 or root:1.1.1.2")
    parser.add_option('-i', '--host', action="store", dest="host", help=u"Connect remote with the host ip")
    parser.add_option('-d', action='store', dest='del_host', help=u"Remove ssh information")
    parser.add_option('-D', '--delete-by-index', action='store_true', dest='del_by_index',
                      help=u"Remove ssh information by index id")
    parser.add_option('-u', '--update', action="store_true", dest="ifupdate")
    # parser.add_option('-')

    (option, args) = parser.parse_args()
    opt_dict = eval(str(option))
    opt_values = opt_dict.values()
    param_len = len(opt_values) - opt_values.count(None)
    output = OutputClient()
    output.set_header(['Index','UserName', 'Host', 'Port', 'Alias'], [7, 17, 17, 10, 30])
    if param_len > 1:
        raise ParamsException('Param Error')
    elif param_len == 0:
        try:
            if len(args) > 0:
                host = args[0]
                ssh_conn = api.get_ssh_connect(host)
                if ssh_conn is not None:
                    api.login(ssh_conn.get('host'), ssh_conn.get('name'), ssh_conn.get('passwd'), ssh_conn.get('port'))
                else:
                    ssh_conns = api.login_fuzzy(host)
                    con_len = len(ssh_conns)
                    if con_len == 0:
                        sys.stdout.write(redStr('No Matched Host\n'))
                        return
                    elif con_len == 1:
                        api.login(ssh_conns[0].get('host'), ssh_conns[0].get('name'), ssh_conns[0].get('passwd'),ssh_conns[0].get('port') )
                        return
                    else:
                        output.set_values(ssh_conns)
                        sys.stdout.write(output.show())
                        sys.stdout.write('\n')
                        ssh_conn = output.select()
                        api.login(ssh_conn.get('host'), ssh_conn.get('name'), ssh_conn.get('passwd'), ssh_conn.get('port'))
                        return
                return
            else:
                ssh_conns = api.list_ssh_connects()
                output.set_values(ssh_conns)
                # print output.show()
                sys.stdout.write(output.show())
                sys.stdout.write('\n')
                if len(ssh_conns) > 0:
                    ssh_conn = output.select()
                    api.login(ssh_conn.get('host'), ssh_conn.get('name'), ssh_conn.get('passwd'), ssh_conn.get('port'))
                return
        except ParamsException as e:
            sys.stdout.write(e.msg)
            sys.stdout.write('\n')
        except TIMEOUT as e:
            sys.stdout.write("Connection Timeout!\n")
        except Exception as e:
            sys.stdout.write(e.message)
            sys.stdout.write('\n')
    else:
        iflist = option.iflist
        add = option.ifadd
        host = option.host
        ifupdate = option.ifupdate
        del_host = option.del_host
        del_by_index = option.del_by_index
        try:
            if iflist:
                ssh_conns = api.list_ssh_connects()
                # print ssh_conns
                output.set_values(ssh_conns)
                sys.stdout.write(output.show())
                sys.stdout.write('\n')
                return
            if add:
                s_l = add.split('@')
                if len(s_l) < 2:
                    sys.stdout.write(
                        redStr('The data format is not correct. Example: <name>@<ip>[:<ssh port>][@<alias>]'))
                    return

                username = s_l[0]
                port = 22
                alias = ''

                if len(s_l) == 3:
                    alias = s_l[2]

                ip_port_arr = s_l[1].split(':')
                host = ip_port_arr[0]
                try:
                    if len(ip_port_arr) == 2:
                        port = int(ip_port_arr[1])
                except Exception, e:
                    sys.stdout.write(
                        redStr('The data format is not correct. Example: <name>@<ip>[:<ssh port>][@<alias>]'))
                    return

                password = getpass.getpass('Input Your Password:')
                api.add_ssh_connect(host, username, password, port, alias)
                # print host, username, password
                return
            if host:
                ssh_conn = api.get_ssh_connect(host)
                if ssh_conn is None:
                    raise Exception("Error: Host %s is not exist!" % host)
                else:
                    api.login(ssh_conn.get('host'), ssh_conn.get('name'), ssh_conn.get('passwd'), ssh_conn.get('port'))
            if ifupdate:
                ssh_conns = api.list_ssh_connects()
                # print ssh_conns
                output.set_values(ssh_conns)
                sys.stdout.write(output.show())
                sys.stdout.write('\n')
                if len(ssh_conns) > 0:
                    ssh_conn = output.select_to_update()
                    username = inputClient.input_username()
                    password = inputClient.input_password()
                    api.update_ssh_connect(ssh_conn.get('host'), username, password)
                    sys.stdout.write(greenStr('Update Successfully!\n'))
            if del_host:
                ssh_conn = api.get_ssh_connect(del_host)
                if ssh_conn is None:
                    # raise Exception("错误: 主机 %s 不存在!" % host)
                    raise Exception("Error: Host %s is not exist!" % host)
                api.del_ssh_connect(del_host)
                # sys.stdout.write('删除成功!\n')
                sys.stdout.write(greenStr('Delete Successfully!'))
            if del_by_index:
                ssh_conns = api.list_ssh_connects()
                # print ssh_conns
                output.set_values(ssh_conns)
                sys.stdout.write(output.show())
                sys.stdout.write('\n')
                if len(ssh_conns) > 0:
                    ssh_conn = output.select_to_del()
                    api.del_ssh_connect(ssh_conn.get('host'))
                    sys.stdout.write(greenStr('Delete Successfully!\n'))
                return
        except ParamsException as e:
            sys.stdout.write(e.msg)
            sys.stdout.write('\n')
        except TIMEOUT as e:
            sys.stdout.write("Connection Timeout!\n")
        except Exception as e:
            sys.stdout.write(e.message)
            sys.stdout.write('\n')


def intur_hander(signal, frame):
    sys.exit(0)


if __name__ == "__main__":
    import signal

    signal.signal(signal.SIGINT, intur_hander)
    main()
