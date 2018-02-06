#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

from __future__ import print_function
from time import sleep
import requests

from utils import APP_KEY, headers, getSign

_logger = None

def setLogger(logger):
    global _logger
    _logger = logger

def sign(ACCESS_KEY):
    params = {'access_key': ACCESS_KEY, 'appkey': APP_KEY}
    params['sign'] = getSign(params)
    r = requests.get('http://live.bilibili.com/mobile/getUser', params=params, headers=headers)
    _logger.debug(r.text)
    json = r.json()
    if json['code'] == 0:
        if json['data']['isSign'] != 1:
            sleep(1)

            params = {'access_key': ACCESS_KEY, 'appkey': APP_KEY, 'scale': 'xxhdpi'}
            params['sign'] = getSign(params)
            r = requests.get('http://live.bilibili.com/AppUser/getSignInfo',
                             params=params, headers=headers)
            _logger.debug(r.text)
            _logger.info("Sign OK!")
        else:
            _logger.info("Already signed!")
    else:
        _logger.error(u'getUser failed! Error code: {} message:{}'.format(json['code'], json['message']))
        if json['code'] == -101: # Not login
            return 1 # Restart

if __name__ == '__main__':
    from logger import getLogger
    setLogger(getLogger())
    sign('ACCESS_KEY')
