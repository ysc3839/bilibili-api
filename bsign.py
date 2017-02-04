#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

from __future__ import print_function
from urllib import urlencode
from hashlib import md5
from time import sleep
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
    r = requests.get('http://live.bilibili.com/mobile/getUser', params=params, headers=headers)
    print(r.text)
    json = r.json()
    if json['code'] == 0 and json['data']['isSign'] != 1:
        sleep(1)

        params = {'access_key': ACCESS_KEY, 'appkey': APP_KEY, 'scale': 'xxhdpi'}
        params['sign'] = get_sign(params)
        r = requests.get('http://live.bilibili.com/AppUser/getSignInfo',
                         params=params, headers=headers)
        print(r.text)

if __name__ == '__main__':
    main()
