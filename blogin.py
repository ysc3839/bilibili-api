#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

from __future__ import print_function
from base64 import b64encode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import requests

from utils import USERNAME, PASSWORD, APP_KEY, headers, getSign

BASE_URL = 'https://passport.bilibili.com/'

_logger = None

def setLogger(logger):
    global _logger
    _logger = logger

def getKey(s):
    params = {'appkey': APP_KEY}
    params['sign'] = getSign(params)
    r = s.post(BASE_URL + 'api/oauth2/getKey', params=params, headers=headers)
    json = r.json()
    if json['code'] != 0:
        _logger.error('getKey failed! Error message:' + json['message'])
        return False
    data = json['data']
    return (data['hash'].encode('ascii'), data['key'].encode('ascii'))

def login(s, username, password, captcha=None):
    params = {'appkey': APP_KEY, 'password': password, 'username': username}
    if captcha:
        params['captcha'] = captcha
    params['sign'] = getSign(params)
    r = s.post(BASE_URL + 'api/oauth2/login', params=params, headers=headers)
    _logger.debug(r.text)
    return r.json()

def rsaEncrypt(password, key_tuple):
    # key_tuple = (_hash, key)
    key = RSA.importKey(key_tuple[1])
    cipher = PKCS1_v1_5.new(key)
    return b64encode(cipher.encrypt(key_tuple[0] + password))

def authInfo(s, access_token):
    params = {'access_token': access_token, 'appkey': APP_KEY}
    params['sign'] = getSign(params)
    r = s.get(BASE_URL + 'api/oauth2/info', params=params, headers=headers)
    _logger.debug(r.text)
    return r.json()

def refreshToken(s, access_token, refresh_token):
    params = {'access_token': access_token, 'appkey': APP_KEY, 'refresh_token': refresh_token}
    params['sign'] = getSign(params)
    r = s.post(BASE_URL + 'api/oauth2/refreshToken', params=params, headers=headers)
    _logger.debug(r.text)
    return r.json()

def logout(s, access_token):
    params = {'access_token': access_token, 'appkey': APP_KEY}
    params['sign'] = getSign(params)
    r = s.post(BASE_URL + 'api/oauth2/revoke', params=params, headers=headers)
    _logger.debug(r.text)
    return r.json()

def doLogin(username, password):
    s = requests.Session()
    key_tuple = getKey(s)
    if key_tuple:
        rjson = login(s, username, rsaEncrypt(password, key_tuple))
        if rjson['code'] == 0:
            # authInfo(s, rjson['data']['access_token'])
            # rjson = refreshToken(s, rjson['data']['access_token'], rjson['data']['refresh_token'])
            # logout(s, rjson['data']['access_token'])
            _logger.info('Access token:' + rjson['data']['access_token'])

            return rjson['data']['access_token']
        else:
            _logger.error('login failed! Error message:' + rjson['message'])

    return None

if __name__ == '__main__':
    from logger import getLogger
    setLogger(getLogger())
    doLogin(USERNAME, PASSWORD)
