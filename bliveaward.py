#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

from __future__ import print_function
from time import time, sleep
import requests

from utils import ACCESS_KEY, APP_KEY, headers, getSign

_logger = None

def setLogger(logger):
    global _logger
    _logger = logger

def main():
    params = {'access_key': ACCESS_KEY, 'appkey': APP_KEY}
    params['sign'] = getSign(params)
    for _ in range(32):
        r = requests.get('http://live.bilibili.com/mobile/freeSilverCurrentTask',
                         params=params, headers=headers)
        _logger.debug(r.text)
        res = r.json()
        if res['code'] == 0:
            wait = res['data']['time_end'] - time() + 5

            _logger.info('Waiting for %d seconds' % wait)
            sleep(wait)

            r = requests.get('http://live.bilibili.com/mobile/freeSilverAward',
                             params=params, headers=headers)
            _logger.debug(r.text)
            j = r.json()
            if j['code'] != 0:
                _logger.info(res['message'])
        else:
            _logger.error('freeSilverCurrentTask returned error! Error message:' + res['message'])
            if res['code'] == -10017 or res['code'] == -101:
                return
            sleep(5)

if __name__ == '__main__':
    from logger import getLogger
    setLogger(getLogger())
    main()
