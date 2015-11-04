import xmlrpclib
import socket
import errno

from libs.helper import get_conns

def mGetAllProcessInfo(configs, section=None, option=None):
    conns = get_conns(configs, section, option)

    for conn in conns:
        server = xmlrpclib.Server(conn['conn'] + '/RPC2')

        try:
            infos = server.supervisor.getAllProcessInfo()
        except socket.error as e:
            print "%s:%s\t%s" % (conn['section'], conn['option'], e)
            continue
        except:
            raise

        if not infos:
            print "%s:%s\tno process" % (conn['section'], conn['option'])
            continue

        for info in infos:
            if info['group'] == info['name']:
                print "%s:%s:%s\t%s\t%s" % \
                    (conn['section'], conn['option'], info['name'], info['statename'], info['description'])
            else:
                print "%s:%s:%s:%s\t%s\t%s" % \
                    (conn['section'], conn['option'], info['group'], info['name'], info['statename'], info['description'])

# https://github.com/Supervisor/supervisor/issues/615
def mGetProcessInfo(configs, section=None, option=None, group=None, name=None):
    conns = get_conns(configs, section, option)

    for conn in conns:
        server = xmlrpclib.Server(conn['conn'] + '/RPC2')

        try:
            info = server.supervisor.getProecssInfo(group + ':' + name)
        except socket.error as e:
            if e.args[0] == errno.ECONNREFUSED:
                print "%s:%s\tconnection refused" % (conn['section'], conn['option'])
                continue

        if info['group'] == info['name']:
            print "%s:%s:%s\t%s\t%s" % \
                (conn['section'], conn['option'], info['name'], info['statename'], info['description'])
        else:
            print "%s:%s:%s:%s\t%s\t%s" % \
                (conn['section'], conn['option'], info['group'], info['name'], info['statename'], info['description'])

def mGetSupervisorVersion(configs, section=None, option=None):
    conns = get_conns(configs, section, option)

    for conn in conns:
        server = xmlrpclib.Server(conn['conn'] + '/RPC2')

        try:
            version = server.supervisor.getSupervisorVersion()
        except socket.error as e:
            if e.args[0] == errno.ECONNREFUSED:
                print "%s:%s\tconnection refused" % (conn['section'], conn['option'])
                continue

        print "%s:%s\t%s" % (conn['section'], conn['option'], version)

def mStartProcess(configs, section=None, option=None, group=None, name=None):
    conns = get_conns(configs, section, option)

    for conn in conns:
        server = xmlrpclib.Server(conn['conn'] + '/RPC2')
        rc = True

        try:
            spec = name
            if group:
                spec = group + ':' + name
            # by default, wait = True
            rc = server.supervisor.startProcess(spec)
        except socket.error as e:
            if e.args[0] == errno.ECONNREFUSED:
                print "%s:%s\tconnection refused" % (conn['section'], conn['option'])
                continue
        except xmlrpclib.Fault as f:
            if f.faultCode == 10:
                print "%s:%s\t no such process" % (conn['section'], conn['option'])
                continue

        print "start %s:%s:%s:%s: %s" % (conn['section'], conn['option'], group, name, rc)

def mStopProcess(configs, section=None, option=None, group=None, name=None):
    conns = get_conns(configs, section, option)

    for conn in conns:
        server = xmlrpclib.Server(conn['conn'] + '/RPC2')
        rc = True

        try:
            spec = name
            if group:
                spec = group + ':' + name
            # by default, wait = True
            rc = server.supervisor.stopProcess(spec)
        except socket.error as e:
            if e.args[0] == errno.ECONNREFUSED:
                print "%s:%s\tconnection refused" % (conn['section'], conn['option'])
                continue
        except xmlrpclib.Fault as f:
            if f.faultCode == 10:
                print "%s:%s\t no such process" % (conn['section'], conn['option'])
                continue

        print "stop %s:%s:%s:%s: %s" % (conn['section'], conn['option'], group, name, rc)

def mShutdown(configs, section=None, option=None):
    conns = get_conns(configs, section, option)

    for conn in conns:
        server = xmlrpclib.Server(conn['conn'] + '/RPC2')
        rc = True

        try:
            rc = server.supervisor.shutdown()
        except socket.error as e:
            if e.args[0] == errno.ECONNREFUSED:
                print "%s:%s\tconnection refused" % (conn['section'], conn['option'])
                continue
        except xmlrpclib.Fault as f:
            if f.faultCode == 10:
                print "%s:%s\t no such process" % (conn['section'], conn['option'])
                continue

        print "shutdown %s:%s: %s" % (conn['section'], conn['option'], rc)
