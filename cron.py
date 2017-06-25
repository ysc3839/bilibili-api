#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

from logger import getLogger
import bsign
import bliveaward

_logger = getLogger()

bsign.setLogger(_logger)
bsign.sign()

bliveaward.setLogger(_logger)
bliveaward.main()
