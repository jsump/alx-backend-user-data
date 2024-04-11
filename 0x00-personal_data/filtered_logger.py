#!/usr/bin/env python3
"""
Module: filtered_logger.py

Return log message obfuscated
"""


import re


def filter_datum(fields, redaction, message, separator):
    """This method returns the message obfuscated"""
    new_msg = re.sub(
            r'({})=([^{}]+)'.format('|'.join(fields), separator),
            lambda m: m.group(1) + '=' + redaction * min(1, len(m.group(2))),
            message)
    return new_msg
