# -*- coding: utf-8 -*-

import os
import importlib

class MeiriBase(object):

    def __init__(self):
        self.plugins = []
        workPath = "/root/QQBot/meiri/meiri/sbin"
        files = os.listdir(workPath)
        for file in files:
            if not os.path.isdir(file):
                self.plugins.append(file[:-3])
    
    def getCmd(self, cmds):
        if cmds[0] in self.plugins:
            cmder = importlib.import_module('sbin.' + cmds[0])
            if len(cmds) == 1:
                return cmder.Create()
            else:
                return cmder.Create(cmds[1])
        else:
            cmder = importlib.import_module('sbin.error')
            return cmder.Create()

Meiri = MeiriBase()
