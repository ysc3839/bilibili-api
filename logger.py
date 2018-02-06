#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

import logging
import logging.handlers

def getLogger():
    logger = logging.getLogger('blive')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logger.addHandler(stream_handler)

    syslog_handler = None
    for addr in ['/dev/log', '/var/run/syslog']:
        try:
            syslog_handler = logging.handlers.SysLogHandler(address=addr)
        except:
            pass
        else:
            break
    if syslog_handler:
        syslog_handler.setFormatter(logging.Formatter('%(filename)s[%(process)d]: [%(levelname)s] %(message)s'))
        logger.addHandler(syslog_handler)

    logger.setLevel(logging.DEBUG)

    return logger
