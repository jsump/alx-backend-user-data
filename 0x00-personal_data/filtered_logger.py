#!/usr/bin/env python3
"""
Module: filtered_logger.py

Return log message obfuscated
"""


import re


def filter_datum(fields, redaction, message, separator):
    """
    This method returns the message obfuscated

    fields: list of strings representing fields to obfuscate
    redaction: string representing by what firls will be obfucated
    message: string representing the log line
    separator: string representing by which character is separating
    all fiends in the log line(message)
    """
    new_msg = re.sub(
            r'({})=([^{}]+)'.format('|'.join(fields), separator),
            lambda m: m.group(1) + '=' + redaction * min(1, len(m.group(2))),
            message)
    return new_msg
