# -*- coding: utf-8 -*-

import subprocess

class syscall(object):

    def __init__(self, cmd):
        self.cmd = cmd

    def execute(self, contact, member):
        try:
            message = subprocess.check_output(self.cmd).read()
            print(message)
        except:
            message = 'Execution failed'
        finally:
            return message

def Create(argv):
    return syscall(argv)