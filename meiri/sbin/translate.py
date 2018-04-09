# -*- coding: utf-8 -*-
import urllib.parse, urllib.request
import hashlib
import urllib
import random
import json

class Baidu:
    def __init__(self):
        self.appid = '20171222000107496'
        self.secretKey = '1Pbd4lbUxSMbl6ROgLTW'
        self.url_baidu = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.fr = 'auto'
        self.to = 'zh'

    def GetUrl(self, text):
        salt = random.randint(32768, 65536)
        sign = self.appid + text + str(salt) + self.secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        if IsChinese(text):
            self.to = 'en'
        else:
            self.to = 'zh'
        url = self.url_baidu + '?appid=' + self.appid + '&q=' + urllib.parse.quote(text) + '&from=' + self.fr + '&to=' + self.to + '&salt=' + str(salt) + '&sign=' + sign
        return url

class translate(object):

    def __init__(self, text):
        self.text = text

    def translateByBaidu(self):
        baidu = Baidu()
        url = baidu.GetUrl(self.text)
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        data = json.loads(content)
        result = str(data['trans_result'][0]['dst'])
        return result

    def execute(self, contact, member):
        try:
            message = '百度翻译的结果:\n' + self.translateByBaidu()
        except:
            message = '翻译失败！'
        finally:
            return message

def IsChinese(text):
    for ch in text:
        if not u'\u4e00' <= ch <= u'\u9fff':
            return False
    return True

def Create(argv):
    return translate(argv)

