# -*- coding: utf-8 -*-

class Plug(object):
    def __init__(self, cmds):
        self.plug = cmds[0]
        self.option = cmds[1]

    def execute(self, contact, member):
        from qqbot import _bot as bot
        try:
            if self.option == 'on':
                bot.Plug(self.plug)
                return self.plug + ' is running...'
            elif self.option == 'off':
                bot.Unplug(self.plug)
                return self.plug + ' is stop now'
        except:
            return 'plug %s not find' % self.plug

def Create(cmds):
    return Plug(cmds.split())