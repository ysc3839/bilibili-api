#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

import os.path
from logger import getLogger
import bsign
import bliveaward
import utils

_logger = getLogger()

bsign.setLogger(_logger)
bliveaward.setLogger(_logger)

ACCESS_KEY = ''

key_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ACCESS_KEY.txt')
with open(key_path, 'r') as f:
    ACCESS_KEY = f.read()

for _ in range(5):
    if bsign.sign(ACCESS_KEY) == 1 or bliveaward.main(ACCESS_KEY) == 1:
        ACCESS_KEY = utils.autoLogin(_logger, key_path)
        continue
    break
