#!/usr/bin/env python2

"""multi

Options:

    -c/--configuration CONFIG -- [TODO] configuration file path (default ./multi.conf)

"""

import cmd

from libs.config import parse_config
from libs.helper import split_spec
from libs.api import *

class Multi(cmd.Cmd):

    def __init__(self, config='./supervisor-multi.ini', completekey='tab', stdin=None, stdout=None):
        self.prompt = 'supervisor-multi> '
        self.configs = parse_config(config)
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
        print 'status <section>:<option>                    Get status for all processes of all groups in a host'
        print 'status <section>:*                           [TODO] Get status for all processes of all groups in all hosts for a section'
        print 'status                                       Get all status infos'

    def do_start(self, arg):
        section, option, group, program = split_spec(arg)

        mStartProcess(self.configs, section, option, group, program)

        #mStartProcessAll(self.configs, section, option, group, program)

    def help_start(self):
        print 'start <section>:<option>:<group>:<name>      Start a single process'

    def do_stop(self, arg):
        section, option, group, program = split_spec(arg)

        mStopProcess(self.configs, section, option, group, program)

        #mStopProcessAll(self.configs, section, option, group, program)

    def help_stop(self):
        print 'stop <section>:<option>:<group>:<name>       Stop a single process'

    def do_restart(self, arg):
        section, option, group, program = split_spec(arg)

        mStopProcess(self.configs, section, option, group, program)
        mStartProcess(self.configs, section, option, group, program)

    def help_restart(self):
        print 'restart <section>:<option>:<group>:<name>        Restart a single process'

    def do_shutdown(self, arg):
        section, option, group, program = split_spec(arg)

        mShutdown(self.configs, section, option)

    def help_shutdown(self):
        print 'shutdown <section>:<option>      Shut the remote supervisord down'
        print 'shutdown <section>               [TODO] Shut the remote supervisords which belong to the section down'

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
