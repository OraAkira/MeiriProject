# -*- coding: utf-8 -*-

import os
import json
import argparse
from qqbot import _bot as bot

class Logger(object):
    count = 0
    def __init__(self, cmds):
        self.argments = cmds.split()
        self.url = 'https://jp.aoiyuki.org/meiri/log/'
        Logger.count += 1
        self.id = Logger.count
        self.path = '/root/QQBot/meiri/meiri/data.json'

    def Load(self):
        with open(self.path, 'r') as f:
            return json.load(f)
    
    def Save(self, data):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def execute(self, contact, member):
        def Create(args):
            if not args.record:
                return '[Error]: Record name can not be empty!'
            if not args.file:
                args.file = '%s.md' % contact.name
            data = self.Load()
            for log in data.values():
                if log['group'] == contact.name and not args.yes:
                    return '[Warning]: This operation will overwrite the original data\nPlease confirm the use of [-y] or [--yes] mandatory override'
            data[self.id] = {
                "record": args.record,
                "status": "dead",
                "group": contact.name,
                "file": args.file,
                "users": {
                    "Meiri": 'white'
                }
            }
            self.Save(data)
            return '[Success]: Create a record named <%s> with %s' % (args.record, args.file)

        def Start(args):
            data = self.Load()
            for log in data.values():
                if log['group'] == contact.name:
                    log['status'] = 'active'
                    self.Save(data)
                    return '[Success]: Record <%s> Started' % log['record']
            return '[Error]: No record found, please create a record first'

        def Pause(args):
            data = self.Load()
            for log in data.values():
                if log['group'] == contact.name:
                    log['status'] = 'pause'
                    self.Save(data)
                    return '[Success]: Record <%s> paused' % log['record']
            return '[Error]: No record found, please create a record first'
        
        def Continue(args):
            data = self.Load()
            for log in data.values():
                if log['group'] == contact.name:
                    log['status'] = 'active'
                    self.Save(data)
                    return '[Success]: Record <%s> continue' % log['record']
            return '[Error]: No record found, please create a record first'

        def Stop(args):
            data = self.Load()
            for log in data.values():
                if log['group'] == contact.name:
                    log['status'] = 'dead'
                    self.Save(data)
                    return '[Success]: Record <%s> stoped' % log['record']
            return '[Error]: No record found, please create a record first'

        def Download(args):
            data = self.Load()
            if args.file:
                return '[Success]: %s%s' % (self.url, args.file)
            for log in data.values():
                if log['group'] == contact.name:
                    return '[Success]: %s%s' % (self.url, log['file'])
            return '[Error]: No record found, please create a record first'

        def Add(args):
            data = self.Load()
            for log in data.values():
                if log['group'] == contact.name:
                    if not args.color:
                        args.color = 'green'
                    log['users'][member.name] = args.color
                    self.Save(data)
                    return '[Success]: Add user %s<%s> success!' % (member.name, args.color)
            return '[Error]: No record found, please create a record first'

        def Set(args):
            data = self.Load()
            for log in data.values():
                if log['group'] == contact.name:
                    if args.group:
                        message = '[Success]: <%s> transferred from %s to %s' % (log['record'], log['group'], args.group)
                        log['group'] = args.group
                        self.Save(data)
                        return message
                    elif member.name not in log['users'].keys():
                        return '[Error]: No user found, please add user to record first'
                    elif args.color:
                        log['users'][member.name] = args.color
                        self.Save(data)
                        return '[Success]: Add user %s<%s> success!' % (member.name, args.color)
                    else:
                        return '[Error]: SyntaxError invalid syntax'
            return '[Error]: No record found, please create a record first'

        def Status(args):
            data = self.Load()
            if args.all:
                message = '[Success]:'
                for log in data.values():
                    message += '\n[%s]: %s<%s>    %s' % (log['record'], log['group'], log['status'], log['file'])
                return message
            else:
                for log in data.values():
                    if contact.name == log['group']:
                        message = '[Success]:\n%s: %s\nfile: %s\nusers:' % (log['record'], log['status'], self.url + log['file'])
                        for (key, value) in log['users'].items():
                            message += '\n    %s: %s' % (key, value)
                        return message
            return '[Error]: No record found, please create a record first'

        parser = argparse.ArgumentParser(prog='record', description='QQ message cloud record', add_help=False)
        subparses = parser.add_subparsers()

        parserCreate = subparses.add_parser('create')
        parserCreate.add_argument('record')
        parserCreate.add_argument('-f', '--file', dest='file')
        parserCreate.add_argument('-y', '--yes', dest='yes', action='store_true')
        parserCreate.set_defaults(func=Create)

        parserStart = subparses.add_parser('start')
        parserStart.set_defaults(func=Start)

        parserStop = subparses.add_parser('stop')
        parserStop.set_defaults(func=Stop)

        parserPause = subparses.add_parser('pause')
        parserPause.set_defaults(func=Pause)

        parserContinue = subparses.add_parser('continue')
        parserContinue.set_defaults(func=Continue)

        parserDownload = subparses.add_parser('download')
        parserDownload.add_argument('-f', '--file', dest='file')
        parserDownload.set_defaults(func=Download)

        parserAdd = subparses.add_parser('add')
        parserAdd.add_argument('-c', '--color', dest='color')
        parserAdd.set_defaults(func=Add)

        parserSet = subparses.add_parser('set')
        setGroup = parserSet.add_mutually_exclusive_group()
        setGroup.add_argument('-c', '--color', dest='color')
        setGroup.add_argument('-g', '--group', dest='group')
        parserSet.set_defaults(func=Set)

        parserStatus = subparses.add_parser('status')
        parserStatus.add_argument('-a', '--all', dest='all', action='store_true')
        parserStatus.set_defaults(func=Status)

        parser.add_argument('-v', '--version', action='store_true')
        parser.add_argument('-h', '--help', action='store_true')

        args = parser.parse_args(self.argments)

        if args.version:
            result = 'Meiri logger v2.0'
        elif args.help:
            result = \
'冥利自动笔记帮助文档:\n\
Example:\n\
*rc create record [-y] [-f filename]\n\
*rc start/stop\n\
*rc pause/continue\n\
*rc download [-f file]\n\
*rc add [-c color]\n\
*rc set [-c color | -g group]\n\
*rc status [-a]\n\
*rc [-v | -h]'
        else:
            result = args.func(args)
        return result

def Create(cmds):
    return Logger(cmds)
'''
class Contact():
    def __init__(self):
        self.qq = 'sadda'
        self.name = 'qqgroup'
class Member():
    def __init__(self):
        self.name = 'name'

if __name__ == '__main__':
    while True:
        cmds = input('please input a command: ')
        if cmds == 'q':
            break
        cmds = Create(cmds)
        print(cmds.execute(Contact(),Member()))
'''