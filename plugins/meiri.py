# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import json
sys.path.append("/root/QQBot/meiri/meiri")
from core import Meiri

SuperUsers = [
    '灯夜'
]

def onQQMessage(bot, contact, member, content):
    cmds = GetCmd(member, content)
    if not cmds:
        data = Load()
        for log in data.values():
            if log['group'] == contact.name and log['status'] == 'active' and member.name in log['users'].keys():
                Write(log['file'], member.name, log['users'][member.name], GetLog(content))
    else:
        cmd = Meiri.getCmd(cmds)
        try:
            result = cmd.execute(contact, member)
        except:
            result = 'SyntaxError: invalid syntax'
        finally:
            bot.SendTo(contact, result)

def GetCmd(member, content):
    if content[0] == '*':
        cmds = content[1:].split(' ', 1)
        if cmds[0] in Meiri.plugins:
            if cmds[0] == 'syscall':
                if not member.name in SuperUsers:
                    return False
            return cmds
        else:
            return False
    else:
        return False

def Load():
    with open('./meiri/data.json', 'r') as f:
        return json.load(f)

def Write(file, name, color, content):
    try:
        with open('./meiri/log/' + file, 'a', encoding='utf-8') as f:
            line = "<font color=gray><%s></font><font color=%s>[%s] %s</font></br>\n" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), color, name, content)
            f.writelines(line)
        print(line)
    finally:
        if f:
            f.close()

def GetLog(text):
    result = ''
    isContent = True
    for ch in text:
        if ch == '(' or ch == '（' or ch == '<' or ch == '[':
            isContent = False
        elif ch == ')' or ch == '）' or ch == '>' or ch == ']':
            isContent = True
        else:
            if isContent:
                result += ch
            else:
                pass
    return result
