#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

from __future__ import print_function
from base64 import b64encode
from urllib import urlencode
from hashlib import md5
from getpass import getpass
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import requests

BASE_URL = 'https://passport.bilibili.com/'

# Get from bilibili android client
APP_KEY = '1d8b6e7d45233436'
APP_SECRET = '560c52ccd288fed045859ed18bffd973'

# Another one
#APP_KEY = '4409e2ce8ffd12b8'
#APP_SECRET = '59b43e04ad6965f34319062b478f83dd'

# Get from https://github.com/WhiteBlue/bilibili-sdk-go/blob/master/test/api_test.go
#APP_KEY = '4ebafd7c4951b366'
#APP_SECRET = '8cb98205e9b2ad3669aad0fce12a4c13'

headers = {'user-agent': 'Mozilla/5.0 BiliDroid/4.34.0 (bbcallen@gmail.com)'}

def getSign(params):
    items = params.items()
    items.sort()
    return md5(urlencode(items) + APP_SECRET).hexdigest()

def getKey(s):
    params = {'appkey': APP_KEY}
    params['sign'] = getSign(params)
    r = s.post(BASE_URL + 'api/oauth2/getKey', params=params, headers=headers)
    json = r.json()
    if json['code'] != 0:
        print(json['message'])
        return False
    data = json['data']
    return (data['hash'].encode('ascii'), data['key'].encode('ascii'))

def login(s, username, password, captcha=None):
    params = {'appkey': APP_KEY, 'password': password, 'username': username}
    if captcha:
        params['captcha'] = captcha
    params['sign'] = getSign(params)
    r = s.post(BASE_URL + 'api/oauth2/login', params=params, headers=headers)
    print(r.text)
    return r.json()

def rsaEncrypt(password, (_hash, key)):
    key = RSA.importKey(key)
    cipher = PKCS1_v1_5.new(key)
    return b64encode(cipher.encrypt(_hash + password))

def authInfo(s, access_token):
    params = {'access_token': access_token, 'appkey': APP_KEY}
    params['sign'] = getSign(params)
    r = s.get(BASE_URL + 'api/oauth2/info', params=params, headers=headers)
    print(r.text)
    return r.json()

def refreshToken(s, access_token, refresh_token):
    params = {'access_token': access_token, 'appkey': APP_KEY, 'refresh_token': refresh_token}
    params['sign'] = getSign(params)
    r = s.post(BASE_URL + 'api/oauth2/refreshToken', params=params, headers=headers)
    print(r.text)
    return r.json()

def logout(s, access_token):
    params = {'access_token': access_token, 'appkey': APP_KEY}
    params['sign'] = getSign(params)
    r = s.post(BASE_URL + 'api/oauth2/revoke', params=params, headers=headers)
    print(r.text)
    return r.json()

def main():
    username = raw_input('Input username:')
    password = getpass('Input password:')
    s = requests.Session()
    key_tuple = getKey(s)
    if key_tuple:
        rjson = login(s, username, rsaEncrypt(password, key_tuple))
        if rjson['code'] == 0:
            authInfo(s, rjson['data']['access_token'])
            rjson = refreshToken(s, rjson['data']['access_token'], rjson['data']['refresh_token'])
            logout(s, rjson['data']['access_token'])

if __name__ == '__main__':
    main()
