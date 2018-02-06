# pylint: disable=I0011,C0103,C0111

from urllib import urlencode
from hashlib import md5

# ACCESS_KEY = '' # Your access key.

USERNAME = ''
PASSWORD = ''

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

def autoLogin(logger, key_path):
    import blogin
    blogin.setLogger(logger)
    key = blogin.doLogin(USERNAME, PASSWORD)

    if not key: exit()

    with open(key_path, 'w') as f:
        f.write(key)

    return key
