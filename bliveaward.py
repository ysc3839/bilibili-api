#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

from __future__ import print_function
from urllib import urlencode
from hashlib import md5
from time import time, sleep
import requests

ACCESS_KEY = '' # Your access key.

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

def get_sign(params):
    items = params.items()
    items.sort()
    return md5(urlencode(items) + APP_SECRET).hexdigest()

def main():
    params = {'access_key': ACCESS_KEY, 'appkey': APP_KEY}
    params['sign'] = get_sign(params)
    while True:
        r = requests.get('http://live.bilibili.com/mobile/freeSilverCurrentTask',
                         params=params, headers=headers)
        res = r.json()
        print(res)
        if res['code'] == 0:
            wait = res['data']['time_end'] - time() + 5
            for i in range(int(wait)):
                print('Waiting for %u seconds' % (wait - i), end='\r')
                sleep(1)

            r = requests.get('http://live.bilibili.com/mobile/freeSilverAward',
                             params=params, headers=headers)
            print(r.text)
        else:
            print(res['message'])
            if res['code'] == -10017 or res['code'] == -101:
                return
            sleep(5)

if __name__ == '__main__':
    main()
