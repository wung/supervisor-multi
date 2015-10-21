#!/usr/bin/env python2

"""multi

Options:

    -c/--configuration CONFIG -- [TODO] configuration file path (default ./multi.conf)

"""

import cmd
import xmlrpclib
import socket
import errno

def split_spec(spec = ''):
    specs = spec.split(':')
    section = option = group = program = None

    # section:option:group:program
    # section:option:group:*
    if len(specs) == 4:
        section, option, group, program = specs
    # section:option:program
    # section:option:*
    elif len(specs) == 3:
        section, option, program = specs
    # section:*
    elif len(specs) == 2:
        section, option = specs
    elif len(specs) == 1:
        pass

    return section, option, group, program

def parseConfig(config):
    import ConfigParser

    configs = {}
    conf = ConfigParser.ConfigParser()
    conf.read(config)

    for section in conf.sections():
        configs[section] = {}
        for option in conf.options(section):
            configs[section][option] = conf.get(section, option)

    return configs

def getConnections(configs, section=None, option=None):
    conns = []
    # all connections
    if section == None:
        for key in configs.keys():
            for k in configs[key].keys():
                conns += [{'section': key, 'option': k, 'conn': configs[key][k]}]
    # one connection
    else:
        try:
            conns = [{'section': section, 'option': option, 'conn': configs[section][option]}]
        except KeyError as e:
            print "no configs"

    # FIXME: unique conns, raise if conns duplicate
    return conns

def mGetAllProcessInfo(configs, section=None, option=None):
    conns = getConnections(configs, section, option)

    for conn in conns:
        server = xmlrpclib.Server(conn['conn'] + '/RPC2')

        try:
            infos = server.supervisor.getAllProcessInfo()
        except socket.error as e:
            if e.args[0] == errno.ECONNREFUSED:
                print "%s:%s\tconnection refused" % (conn['section'], conn['option'])
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
    conns = getConnections(configs, section, option)

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
    conns = getConnections(configs, section, option)

    for conn in conns:
        server = xmlrpclib.Server(conn['conn'] + '/RPC2')

        try:
            version = server.supervisor.getSupervisorVersion()
        except socket.error as e:
            if e.args[0] == errno.ECONNREFUSED:
                print "%s:%s\tconnection refused" % (conn['section'], conn['option'])
                continue

        print "%s:%s\t%s" % (conn['section'], conn['option'], version)

class Multi(cmd.Cmd):

    def __init__(self, config='./multi.ini', completekey='tab', stdin=None, stdout=None):
        self.prompt = 'supervisor-multi> '
        self.configs = parseConfig(config)
        cmd.Cmd.__init__(self, completekey, stdin, stdout)

    def do_status(self, arg):
        section, option, group, program = split_spec(arg)

        if group == None or program == None:
            mGetAllProcessInfo(self.configs, section, option)
        else:
            mGetProcessInfo(self.configs, section, option, group, program)

    def help_status(self):
        print 'status <section>:<option>:<group>:<name>     Get status for a single process'
        print 'status <section>:<option>:<name>             Get status for a single process'
        print 'status <section>:<option>:<group>:*          [TODO] Get status for all processes in a group'
        print 'status <section>:<option>:*                  [TODO] Get status for all processes of all groups in a host'
        print 'status <section>:<option>                    Get status for all processes of all groups in a host'
        print 'status <section>:*                           [TODO] Get status for all processes of all groups in all hosts for a section'
        print 'status                                       Get all status infos'

    def do_version(self, arg):
        section, option, group, program = split_spec(arg)
        mGetSupervisorVersion(self.configs, section, option)

    def help_version(self):
        print 'version <section>:<option>       Show the version of the remote supervisord'
        print 'version                          Show all the version infos'

    def do_EOF(self, line):
        return True

    def help_EOF(self):
        print 'To quit, type ^D'

    def help_help(self):
        print 'help <action>        Print help for <action>'
        print 'help                 Print a list of available actions'

Multi().cmdloop()
