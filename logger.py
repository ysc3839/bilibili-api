#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

import logging
import logging.handlers

def getLogger():
    logger = logging.getLogger('blive')

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

    syslogHandler = logging.handlers.SysLogHandler(address='/dev/log')
    syslogHandler.setFormatter(
        logging.Formatter('%(filename)s[%(process)d]: [%(levelname)s] %(message)s'))

    logger.addHandler(streamHandler)
    logger.addHandler(syslogHandler)

    logger.setLevel(logging.DEBUG)

    return logger
